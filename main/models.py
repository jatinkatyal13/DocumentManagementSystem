from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

FLAG_OPTIONS = (
    (1, 'open'),
    (2, 'restricted')
)

USER_PERMISSION_FLAG_OPTIONS = (
    (1, 'READ'), # 01
    (2, 'WRITE'), # 10
    (3, 'READ/WRITE') # 11
)

class File(models.Model):
    name = models.CharField(max_length = 1024)
    latestVersion = models.ForeignKey('FileVersion', blank = True, null = True, on_delete = models.CASCADE, related_name = 'latestFile')
    readFlag = models.IntegerField(choices = FLAG_OPTIONS, default = 1)
    writeFlag = models.IntegerField(choices = FLAG_OPTIONS, default = 2)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name

class Document(models.Model):
    url = models.FileField()
    markdown = models.TextField(blank = True, default = '')
    docType = models.CharField(max_length = 256)

class FileVersion(models.Model):
    file = models.ForeignKey('File', on_delete = models.CASCADE)
    document = models.ForeignKey('Document', on_delete = models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class FileUserPermission(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    file = models.ForeignKey('File', on_delete = models.CASCADE)
    permissionFlag = models.SmallIntegerField(choices = USER_PERMISSION_FLAG_OPTIONS)

class FileGroupPermission(models.Model):
    group = models.ForeignKey('Group', on_delete = models.CASCADE)
    file = models.ForeignKey('File', on_delete = models.CASCADE)
    permissionFlag = models.SmallIntegerField(choices = USER_PERMISSION_FLAG_OPTIONS)

class Group(models.Model):
    name = models.CharField(max_length = 1024)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class UserAccessLog(models.Model):
    file = models.ForeignKey('File', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    operation = models.IntegerField(choices = FLAG_OPTIONS)
    fileOldVersion = models.ForeignKey('FileVersion', on_delete = models.CASCADE, null = True, blank = True, related_name = 'oldLog')
    fileNewVersion = models.ForeignKey('FileVersion', on_delete = models.CASCADE, null = True, blank = True, related_name = 'newLog')

# Signals
@receiver(post_save, sender=FileVersion)
def file_version_save_handler(instance, **kwargs):
    file = instance.file
    file.latestVersion = instance
    file.save()
