from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormMixin
from contact.models import UserProfile

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'account/profile/personal_page.html'

    def get_queryset(self):
        user1 = self.request.user
        msg_count = dict()
        messages = ChatMessage.objects.filter(Q(thread__second=user1) | Q(thread__first=user1), is_readed=False).exclude(user=user1)
        for msg in messages:
            try:
                msg_count[msg.user.username] +=1
            except:
                msg_count[msg.user.username] =1
        return msg_count


# class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
#     template_name = 'chat/thread_new.html'
#     form_class = ComposeForm
#     success_url = './'
#
#     def get_object(self):
#         user_slug  = self.kwargs.get("slug")
#         post_num = self.kwargs.get("post_num")
#         print(post_num)
#         user_profile = self.request.user.profile
#         other_username = get_object_or_404(UserProfile, slug=user_slug)
#         if other_username.user in user_profile.friends.all():
#             obj, created    = Thread.objects.get_or_new(user_profile, other_username)
#             if obj:
#                 messages = ChatMessage.objects.filter(thread=obj, is_readed=False).exclude(user=self.request.user.profile)
#                 for item in messages:
#                     item.is_readed = True
#                     item.save()
#             if obj == None:
#                 raise Http404
#             return obj.chatmessage_set.all()[:post_num]
#         else:
#             raise Exception('Vy ne mojete Otp soobsheniya polzovatelem kotorye ne yavlyayutsya vashim drugom')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         thread = self.get_object()
#         print(thread)
#         user = self.request.user.profile
#         message = form.cleaned_data.get("message")
#         ChatMessage.objects.create(user=user, thread=thread, message=message)
#         return super().form_valid(form)
#

class JsonResponsePrivetMessages(LoginRequiredMixin, FormMixin, View):
    form_class = ComposeForm

    def get(self, *args, **kwargs):
        user_slug = self.kwargs['slug']
        user_profile = self.request.user.profile
        other_username = get_object_or_404(UserProfile, slug=user_slug)
        if other_username.user in user_profile.friends.all():
            obj, created = Thread.objects.get_or_new(user_profile, other_username)
            if obj:
                messages = ChatMessage.objects.filter(thread=obj, is_readed=False).exclude(user=self.request.user.profile)
                for item in messages:
                    item.is_readed = True
                    item.save()
            upper = 10
            msg_size = len(obj.chatmessage_set.all())
            json = list()
            context = dict()
            try:
                upper = self.kwargs['number']
                if upper:
                    lower = upper - 10
                    json = list(obj.chatmessage_set.all().order_by('-timestamp')[lower:upper].values('user_id', 'message','timestamp'))
                    for item in json:
                        if item['user_id'] == user_profile.id:
                            item['sender'] = 'align-self-flex-end'
                        else:
                            item['sender'] = ''
                        item['user_name'] = UserProfile.objects.get(id=item['user_id']).first_name
                        item['user_avatar'] = UserProfile.objects.get(id=item['user_id']).avatar.url
                    context['load_more'] = False if upper >= msg_size else True;
                    return JsonResponse({'new_data': json, 'load_more': context}, safe=False)
            except:
                for item in list(obj.chatmessage_set.all().order_by('-timestamp')[0:upper].values('user_id',
                                                                                                  'message','timestamp')):
                    json.insert(0, item)
                for item in json:
                    if item['user_id'] == user_profile.id:
                        item['sender'] = 'align-self-flex-end'
                    else:
                        item['sender'] = ''
                    item['user_name'] = UserProfile.objects.get(id=item['user_id']).first_name
                    item['user_avatar'] = UserProfile.objects.get(id=item['user_id']).avatar.url
                context['load_more'] = False if upper >= msg_size else True;
            return JsonResponse({'data': json, 'load_more': context}, safe=False)
        else:
            return Http404

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        other_user = get_object_or_404(UserProfile, slug=slug)
        user = self.request.user.profile
        thread, created = Thread.objects.get_or_new(user, other_user)
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        last_msg = ChatMessage.objects.all().last()
        json = list(thread.chatmessage_set.filter(id=last_msg.id).values('user_id', 'message', 'timestamp'))
        new_messages_from = thread.chatmessage_set.filter(is_readed=False).exclude(user=user)
        if len(new_messages_from) > 0:
            for user_messsage in list(thread.chatmessage_set.filter(is_readed=False).exclude(user=user).values('user_id', 'message', 'timestamp')):
                json.insert(0, user_messsage)
            for item in new_messages_from:
                item.is_readed = True
                item.save()
        for item in json:
            if item['user_id'] == user.id:
                item['sender'] = 'align-self-flex-end'
            else:
                item['sender'] = ''
            item['user_name'] = UserProfile.objects.get(id=item['user_id']).first_name
            item['user_avatar'] = UserProfile.objects.get(id=item['user_id']).avatar.url
        return JsonResponse({'data': json}, safe=False)

