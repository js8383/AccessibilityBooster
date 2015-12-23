from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from accTool.validators import validate_file_extension


# Create your models here.
class ParsedImage(models.Model):
    order = models.IntegerField(default=0)
    cacheLink = models.TextField()
    altText = models.TextField(blank=True)

class ebd_file(models.Model):
	file_link = models.FileField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

class Document(models.Model):
    docfile = models.FileField(upload_to='upload/pdf/')
    def extension(self):
    	import os
        name, extension = os.path.splitext(self.docfile.name)
        return extension

class Headings(models.Model):
    order = models.IntegerField(default=0)
    heading = models.TextField()

class Metadata(models.Model):
    k = models.TextField()
    v = models.TextField()
    order = models.IntegerField(default=0)