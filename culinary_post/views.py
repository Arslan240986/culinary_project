from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from contact.models import UserProfile
from .models import CulinaryPost, PostLike
from .forms import CulinaryPostModelForm, PostCommentModelForm


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
            return redirect('posts:culinary_post_view')
        else:
            print(p_form.errors)
            context = {'p_form': p_form}
            return render(request, 'meals/posts/posts_add.html', context)

    context = {
        'p_form': p_form,
    }
    return render(request, 'meals/posts/posts_add.html', context)


@login_required
def posts_comment_create_and_list_view(request):
    qs = CulinaryPost.objects.all()
    profile = get_object_or_404(UserProfile, user=request.user)

    c_form = PostCommentModelForm()

    if request.POST:
        c_form = PostCommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = get_object_or_404(CulinaryPost, id=request.POST.get('post_id'))
            instance.save()
            c_form = PostCommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'c_form': c_form,
    }
    return render(request, 'meals/posts/culinary_posts.html', context)


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
    return redirect('posts:culinary_post_view')


class CulinaryPostDeleteView(LoginRequiredMixin, DeleteView):
    model = CulinaryPost
    template_name = 'meals/posts/post_delete.html'
    success_url = reverse_lazy('posts:culinary_post_view')

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
    template_name = 'meals/posts/post_update.html'
    success_url = reverse_lazy('posts:culinary_post_view')

    def form_valid(self, form):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "Вы не являетесь автором данного поста ")
            return super().form_invalid(form)