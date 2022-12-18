from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.author.username, self.title)

    def get_excerpt(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passport_series = models.CharField(max_length=4, blank=True)
    passport_number = models.CharField(max_length=6, blank=True)
    patronymic = models.CharField(max_length=20)
    phone = models.CharField(max_length=11, blank=True)
    policy = models.CharField(max_length=16, blank=True)
    insurance_number = models.CharField(max_length=13, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
