from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
import logging
from google.appengine.ext import db


class AppContent(models.Model):
    name = models.CharField(max_length=64)
    caption = models.CharField(max_length=64)
    language = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["name"]
        
class AppTemplate(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["name"]

class AppModule(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["name"]
    
class AppView(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    pagename = models.CharField(max_length=64)
    caption = models.CharField(max_length=64)
    is_redirect = models.BooleanField()
    module = models.ForeignKey(AppModule, null=False, blank=False)
    template = models.ForeignKey(AppTemplate, null=True, blank=True)
    default_content = models.ForeignKey(AppContent, null=True, blank=True)
    def __unicode__(self):
        return "%s/%s" % (self.module.name, self.name,)    
    class Meta:
        ordering = ["url"]
    
class AppDocument(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64, null=True, blank=True)
    content_type = models.CharField(max_length=64, null=True, blank=True)
    content_length = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    blob_key = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name
    
    def fill_from_form(self, cd, blobinfo=None):
        self.name = cd["name"]
        self.title = cd["title"]        
        if blobinfo:
            self.content_type = blobinfo.content_type
            self.file_name = blobinfo.filename
            self.content_length = blobinfo.size
            self.blob_key = blobinfo.key()
            if not self.name:
                self.name = blobinfo.filename
    class Meta:
        ordering = ["name"]

class AppBlobStore(db.Model):
    content_type = db.StringProperty()
    size = db.IntegerProperty()
    content = db.BlobProperty()
    filename = db.StringProperty()

    def fill_from_form(self, file):
        if file:
            self.content = db.Blob(file.read())
            self.content_type = file.content_type
            self.filename = file.name
            self.size = file.size
    class Meta:
        ordering = ["filename"]

class AppMessage(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=64)
    accepted = models.BooleanField()
    def __unicode__(self):
        return self.name
    
class AppTextFile(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField()
    content_type = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ["name"]
    
def get_documents():
    return AppDocument.objects.all()

def get_messages(accepted=True):
    return AppMessage.objects.filter(accepted=accepted);

def get_content_by_tile(tile):
    memkey = "%s-content" % tile
    data = cache.get(memkey)
#    data = None
    if data is not None:
        logging.info("#### %%%%%%%%%%%%%%%% SERVING FROM CACHE: :D")
        return data
    else:
        row = AppContent.objects.filter(name=tile)[:1]
        if row:
            cache.set(memkey, row[0], 3600)
            return row[0]
        else:
            return None

def get_content_string_by_tile(tile):
    content = get_content_by_tile(tile)
    if content:
        return content.content, content.id
    else:
        return "", -1

def get_static_file(key):
    data = cache.get(key)
    if data is not None:
        return data
    else:
        data = AppTextFile.objects.filter(name=key)[:1]
        if data:
            cache.set(key, data[0], 3600)
            return data[0]
        else:
            return AppTextFile()

def get_template_by_model_view(module, view):
    key = "%s-%s" % (module, view)
    data = cache.get(key)
#    data = None
    if data is not None:
        logging.info("#### %%%%%%%%%%%%%%%% SERVING FROM CACHE: :D")
        return data
    else:
        try:
            appmodule = AppModule.objects.filter(name=module)[0]
            row = AppView.objects.filter(module=appmodule, name=view)[0]
            logging.info(row)
            if row:
                cache.set(key, row, 3600)
                return row
            else:
                return None
        except IndexError:
            return None
