from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from contact.models import UserProfile
from hitcount.models import HitCount
from hitcount.views import HitCountDetailView, HitCountMixin

from .models import CulinaryPost, PostLike
from .forms import CulinaryPostModelForm, PostCommentModelForm
from culinary_recipe.utils import getMonth
from culinary_recipe.views import watermark_photo


@login_required
def posts_add(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    p_form = CulinaryPostModelForm()

    if request.POST:
        p_form = CulinaryPostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            watermark_photo(instance.image, str(instance.image), 'static/image/logo_header.png', position=(10, 10))
            messages.success(request, 'Спасибо за участие! Ваш пост будет добавлен на сайт после прохождения модерации.')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            context = {'p_form': p_form}
            return render(request, 'culinary_post/posts_add.html', context)
    context = {
        'p_form': p_form,
    }
    return render(request, 'culinary_post/posts_add.html', context)


def post__list_view(request):
    qs = CulinaryPost.objects.all().filter(moderator=True)
    context = {
        'qs': qs,
    }
    return render(request, 'culinary_post/culinary_posts.html', context)


class AddCommentToPost(View):
    """Добавления коментарии к блюде"""
    def post(self, request, pk):
        context = {'status': False}
        form = PostCommentModelForm(request.POST)
        post = get_object_or_404(CulinaryPost, id=pk)
        user = request.user
        if form.is_valid():
            form = form.save(commit=False)
            form.author = get_object_or_404(UserProfile, user=user)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.save()
            context = {
                'status': True
            }
        return JsonResponse(context, safe=False)


class CulinaryPostDetailView(HitCountDetailView):
    model = CulinaryPost
    template_name = 'culinary_post/post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        hit_count = HitCount.objects.get_for_object(post)
        HitCountMixin.hit_count(request, hit_count)
        form = PostCommentModelForm()
        comments = post.post_comments.all().filter(status=True)
        comment_size = len(comments)
        context = dict()
        try:
            upper = self.kwargs['number']
            if upper:
                low = upper - 5
                comments_number = list(reversed(comments.values('id', 'parent_id', 'author_id', 'created', 'text', 'level')))[low:upper]
                if not comments_number[-1]['level'] == 0:
                    while not comments_number[-1]['level'] == 0:
                        upper += 1
                        comments_number = list(
                            reversed(comments.values('id', 'parent_id', 'author_id', 'created', 'text', 'level')))[
                                          low:upper]
                for comment in comments_number:
                    date_time = str(comment['created']).split(' ')
                    date = date_time[0].split('-')
                    time = date_time[1].split(':')
                    comment['created'] = f'{date[2]} {getMonth(date[1])} {date[0]} г. {time[0]}:{time[1]}'
                    comment['user_name'] = UserProfile.objects.get(id=comment['author_id']).first_name
                    comment['user_avatar'] = UserProfile.objects.get(id=comment['author_id']).avatar.url
                    comment['user_personal_page'] = UserProfile.objects.get(id=comment['author_id']).get_user_profile_detail_absolute_url()

                context['load_more'] = False if upper >= comment_size else True;
            return JsonResponse({'new_data': comments_number, 'load_more': context}, safe=False)
        except:
            first_num = 5
            ne = list(reversed(comments))[:first_num]
            new_comments = list(reversed(ne))
            if new_comments:
                while not new_comments[0].level == 0:
                    first_num += 1
                    ne = list(reversed(comments))[:first_num]
                    new_comments = list(reversed(ne))
        context = {
                    'post': post,
                    'form': form,
                    'post_comments': new_comments,
                    'post_comments_len': len(new_comments),
                    'comment_size': comment_size
                   }
        return render(request, self.template_name, context)




@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = get_object_or_404(CulinaryPost, id=post_id)
        profile = get_object_or_404(UserProfile, user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = PostLike.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post_obj.save()
        like.save()
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('culinary_post:culinary_post_view')


class CulinaryPostDeleteView(LoginRequiredMixin, DeleteView):
    model = CulinaryPost
    template_name = 'culinary_post/post_delete.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(CulinaryPost, id=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request,
                             'Вы не являетесь автором данного поста')
        return obj


class CulinaryPostUpdateView(LoginRequiredMixin, UpdateView):
    model = CulinaryPost
    form_class = CulinaryPostModelForm
    template_name = 'culinary_post/post_update.html'

    def get(self, request, *args, **kwargs):
        if not self.get_object().author == self.request.user.profile:
            context = {
                'notification': 'Упс! Вы не являетесь автором данного поста!',
                'link_to_back': f'{self.request.user.profile.get_personal_absolute_url()}'
            }
            return render(request, 'includes/notification.html', context)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context = self.get_context_data()
        print('form', form.instance.author)
        if form.instance.author == profile:
            print('bool', form.instance.author == profile)
            instance = form.save(commit=False)
            instance.save()
            print('image' in self.request.FILES)
            if 'image' in self.request.FILES:
                watermark_photo(instance.image, str(instance.image), 'static/image/logo_header.png', position=(10, 10))
            messages.success(self.request, 'Спасибо за участие! Ваш пост будет добавлен на сайт после прохождения модерации.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            form.add_error(None, "Вы не являетесь автором данного поста ")
            return super().form_invalid(form)