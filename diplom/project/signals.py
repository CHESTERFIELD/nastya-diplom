# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import *
#
# @receiver(pre_save, sender=User)
# def create_user_custom_user_pre_save(sender, instance, **kwargs):
#     if instance.is_valid():
#         pass
#     else:
#         raise ValidationError
#
#
# @receiver(post_save, sender=User)
# def create_user_custom_user(sender, instance, created, **kwargs):
#     if created:
#         CustomUser.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_custom_user(sender, instance, **kwargs):
#     instance.customuser.save()
