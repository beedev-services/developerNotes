from django.db import models
from django.core.validators import RegexValidator
import re
from django.db.models.fields import BooleanField, CharField
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'

        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email Address already in use'

        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] = 'Username already in use'

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=45, unique=True)
    level = models.IntegerField(default=0)
    password = models.CharField(max_length=45)

    objects = UserManager()

    userCreatedAt = models.DateTimeField(auto_now_add=True)
    userUpdatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username

class Profile(models.Model):
    discord = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profileImgs', default='bee.jpg')
    def __str__(self):
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class Stack(models.Model):
    stackName = models.CharField(max_length=255)

class Note(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    private = models.BooleanField(default=False)
    code = models.TextField(blank=True)
    upvote = models.IntegerField(default=0)
    resourceLink = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(User, related_name='noteUser', on_delete=CASCADE)
    stack = models.ForeignKey(Stack, related_name='noteStack', on_delete=CASCADE)
    def __str__(self):
        return self.subject

class Upload(models.Model):
    uploadName = models.CharField(max_length=255, blank=True)
    upload = models.FileField(upload_to='docs', default='bee.jpg')
    note = models.OneToOneField(Note, unique=True, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.note.subject} Upload'

def create_note_upload(sender, instance, created, **kwargs):
    if created:
        Note.objects.create(note=instance)
        post_save.connect(create_note_upload, sender=Note)

class Comment(models.Model):
    comment = models.TextField()
    commentCode = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    resourceUrl = models.CharField(max_length=255, blank=True)
    commenter = models.ForeignKey(User, related_name='commentUser', on_delete=CASCADE)
    note = models.ForeignKey(Note, related_name='commentNote', on_delete=CASCADE)
    commentCreatedAt = models.DateTimeField(auto_now_add=True)
    commentUpdatedAt = models.DateTimeField(auto_now=True)