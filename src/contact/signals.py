from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserProfile, Relationship
from django.contrib.auth.models import User
from private_chat.models import Thread


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_accept_friend(sender, instance, created, **kwargs):
    print('signals', instance)
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    try:
        thread = Thread.objects.get(first=sender, second=receiver)
        thread.delete()
    except:
        thread = Thread.objects.get(first=receiver, second=sender)
        thread.delete()
    sender.save()
    receiver.save()


# @receiver(post_save)
# def social_login_fname_lname_profilepic(sociallogin, user, **kwargs):
#     preferred_avatar_size_pixels=256
#     picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
#         hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
#         preferred_avatar_size_pixels
#     )
#     print('arslan', sociallogin)
#     print('user', user)
#     if sociallogin:
#         # Extract first / last names from social nets and store on User record
#         if sociallogin.account.provider == 'twitter':
#             name = sociallogin.account.extra_data['name']
#             user.first_name = name.split()[0]
#             user.last_name = name.split()[1]
#
#         if sociallogin.account.provider == 'facebook':
#             f_name = sociallogin.account.extra_data['first_name']
#             l_name = sociallogin.account.extra_data['last_name']
#             if f_name:
#                 user.first_name = f_name
#             if l_name:
#                 user.last_name = l_name
#
#             #verified = sociallogin.account.extra_data['verified']
#             picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
#                 sociallogin.account.uid, preferred_avatar_size_pixels)
#
#         if sociallogin.account.provider == 'google':
#
#             f_name = sociallogin.account.extra_data['given_name']
#             l_name = sociallogin.account.extra_data['family_name']
#             print('provider', f_name)
#             if f_name:
#                 user.first_name = f_name
#             if l_name:
#                 user.last_name = l_name
#             #verified = sociallogin.account.extra_data['verified_email']
#             picture_url = sociallogin.account.extra_data['picture']
#
#     user.save()
#     profile = UserProfile(user=user, avatar_url=picture_url)
#     profile.save()