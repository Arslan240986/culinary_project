from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .tasks import send_subscribe

from .models import ContactSubscribe, UserProfile, Relationship
from .forms import ProfileEditForm, ContactSubscribeForm
from culinary_recipe.models import Dish, DishComment
from private_chat.models import ChatMessage, Thread


@login_required
def edit(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
        if profile_form.is_valid():
            if request.FILES:
                user_profile.avatar.delete()
            profile_form.save()
            return redirect(request.user.profile.get_personal_absolute_url())
        else:
            context = {'profile_form': profile_form}
            return render(request, 'contact/profile_page.html', context)
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'contact/profile_page.html', {'profile_form': profile_form, 'profile': user_profile})


@login_required
def personal_page(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    profile_form = ProfileEditForm(instance=request.user.profile)
    meals = Dish.objects.filter(author__profile=user_profile, draft=False, moderator=True).order_by('-created')
    meals_not_added = Dish.objects.filter(author__profile=user_profile, draft=False, moderator=False)
    meals_draft = Dish.objects.filter(author__profile=user_profile, draft=True)
    reviews = DishComment.objects.filter(author__profile=user_profile)
    threads = Thread.objects.by_user(user_profile)
    total_msg = 0
    for thread in threads:
        msg = ChatMessage.objects.filter(thread=thread, is_readed=False).exclude(user=user_profile).count()
        total_msg += msg
    context = {
        'posts' : user_profile.get_total_posts_moderator_true(),
        'posts_false': user_profile.get_total_posts_moderator_false(),
        'msg_count': total_msg,
        'meals': meals,
        'meals_not_added': meals_not_added,
        'meals_draft': meals_draft,
        'reviews': reviews,
        'profile': user_profile,
        'profile_form': profile_form
    }
    return render(request, 'contact/profile_page.html', context)


@login_required
def personal_draft_page(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    meals = Dish.objects.filter(author__profile=profile, draft=True)
    return render(request, 'contact/personal_draft_page.html', {'meals': meals,})


def contact_view(request):
    """Форма подписки"""
    email_form = ContactSubscribeForm()
    if request.method == 'POST':
        email_form = ContactSubscribeForm(request.POST)
        if email_form.is_valid():
            email_form.save()
            send_subscribe.delay(email_form.instance.email)
            messages.success(request, 'Вы успешно добавили имаил на подписку')
            return JsonResponse({'status': True}, safe=False)
        else:
            messages.error(request, 'Данный имаил уже добавлен')
            return JsonResponse({'status': False}, safe=False)
    return render(request, 'meals/category_list.html', {'contact_form': email_form})


@login_required
def add_dishes(request):
    """Добавляет в кулинарную книгу ретцепты"""
    id = request.POST.get('id')
    meal = get_object_or_404(Dish, id=id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if id in [i.id for i in profile.dishes.all()]:
        meal.dish_added = True
        meal.save()
    if request.method == 'POST':
        context = {
            'dish_added': meal.dish_added,
        }
        if meal.dish_added :
            meal.dish_added = False
            profile.dishes.remove(id)
            profile.save()
            meal.save()
            context['count'] = request.user.profile.get_total_book()
        else:
            meal.dish_added = True
            profile.dishes.add(id)
            profile.save()
            meal.save()
            context['count'] = request.user.profile.get_total_book()
        if request.is_ajax():
            return JsonResponse(context)


@login_required()
def user_dish_book(request, slug):
    """Кулинарная книга"""
    profile = get_object_or_404(UserProfile, slug=slug)
    if request.method == "GET":
        if request.user == profile.user:
            dishes = profile.dishes.all()
            return render(request, 'contact/dish_book.html', {'dishes': dishes})
        else:
            return HttpResponse('Wy pytayetes voyti ne svoyu knigu')


@login_required
def invites_received_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    result = list(map(lambda x: x.sender, qs))
    context = {
        'qs': result
    }
    return render(request, 'contact/my_invites.html', context)


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = get_object_or_404(UserProfile, id=pk)
        receiver = get_object_or_404(UserProfile, user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('contact:my_invites_view')


@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = get_object_or_404(UserProfile, id=pk)
        receiver = get_object_or_404(UserProfile, user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('contact:my_invites_view')


def invite_profiles_list_view(request):
    user = request.user
    qs = UserProfile.objects.get_all_profile_to_invite(user)

    context = {
        'qs': qs
    }
    return render(request, 'contact/to_invite_list.html', context)


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'contact/profile_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(UserProfile, slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user = get_object_or_404(User, id=self.request.user.id)
        user_profile = self.get_object()
        recipes = user_profile.user.dish.all().filter(moderator=True, draft=False)
        profile_request_user = UserProfile.objects.get(user=request_user)
        rel_r = Relationship.objects.filter(sender=profile_request_user)
        rel_s = Relationship.objects.filter(receiver=profile_request_user)
        context['rel_receiver'] = [item.receiver.user for item in rel_r]
        context['rel_sender'] = [item.sender.user for item in rel_s]
        context['is_empty'] = False
        context['recipes'] = recipes
        context['posts'] = self.get_object().get_total_posts()
        context['len_posts'] = True if len(self.get_object().get_total_posts()) > 0 else False
        return context


class ProfileFriendList(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "contact/profile_friends_list.html"
    context_object_name = 'friends'

    def get_queryset(self):
        profile = UserProfile.objects.get(slug=self.kwargs['slug'])
        friends = profile.friends.all()
        friends_dict = {}
        for friend in friends:
            count = friend.profile.chatmessage_set.filter(Q(thread__first=profile) | Q(thread__second=profile), is_readed=False).count()

            try:
                friends_dict[friend.profile]+=count
            except:
                friends_dict[friend.profile] = count
        return friends_dict


class ProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'contact/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = UserProfile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.request.user.id)
        profile = UserProfile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        context['rel_receiver'] = [item.receiver.user for item in rel_r]
        context['rel_sender'] = [item.sender.user for item in rel_s]
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


@login_required
def send_invitation(request):
    """Sends invitation for friends"""

    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = get_object_or_404(UserProfile, user=user)
        receiver = get_object_or_404(UserProfile, pk=pk)

        Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('contact:user_profile')


@login_required
def remove_from_friends(request):
    """Remove friends relationship"""

    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = get_object_or_404(UserProfile, user=user)
        receiver = get_object_or_404(UserProfile, pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('contact:user_profile')