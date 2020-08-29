from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
# Create your models here.

class MyProfile(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18), MaxValueValidator(100)])
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, default='single', choices=(("single", "single"), \
                                                                        ("married", "married"), \
                                                                        ("widow", "widow"), \
                                                                        ("separated","separated"), \
                                                                        ("commited", "commited")
                                                                        ))
    gender = models.CharField(max_length=15, default='male', choices=(("male", "male"), \
                                                                        ("frmale", "female")
                                                                        ))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]\d{9}$")], \
                                max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='profile/images/', null=True)

    def __str__(self):
        return "%s" % self.user



class MyPost(models.Model):
    pic = models.ImageField(upload_to='post/images/', null=True)
    subject = models.CharField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % self.subject

class PostComment(models.Model):
    post = models.ForeignKey(MyPost, on_delete=models.CASCADE)
    msg = models.TextField()
    commented_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(("racist", "racist"),("abusing","abusing")))

    def __str__(self):
        return self.msg


class PostLike(models.Model):
    post = models.ForeignKey(MyPost, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.liked_by)


class FollowUser(models.Model):
    profile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='profile')
    followed_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='followed_by')

    def __str__(self):
        return (f"{self.profile} is followed by {self.followed_by}")

