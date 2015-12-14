from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
import logging
from google.appengine.ext import db

PUBLICATION_CHOICES = (
    ('1.Book', 'Book'),
    ('2.Journal', 'Journal'),
    ('3.Conference', 'Conference'),
    ('4.Technical Report', 'Technical Report'),
    ('5.Submitted', 'Submitted'),
    ('6.In-Preparation', 'In-Preparation'),
    ('7.Others', 'Others'),
)

PUBLICATION_STATUS_CHOICES = (
    ('Published', 'Published'),
    ('Ongoing', 'Ongoing'),
    ('Accepted', 'Accepted'),
    ('Others', 'Others'),
)

RANK_ALPHA = (
    ('A', 'A'),
    ('A*', 'A*'),
    ('B', 'B'),
    ('C', 'C'),
    ('-', '-'),
)

RANK_NUM = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('-', '-'),
)



class News(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True) 
    when= models.DateField()
    content = models.TextField()
    kind = models.CharField(max_length=64, null=True, blank=True) 
    def __unicode__(self):
        return self.title
    def fill_from_form(self, cd):
        self.title = cd["title"]
        self.content = cd["content"]
        self.when = cd["when"] 
        self.kind = cd["kind"]
    class Meta:
        ordering = ["when"]

class Link(models.Model):
    name = models.CharField(max_length=64)
    pass

class ConferenceCategory(models.Model):
    name = models.CharField(max_length=64)
    full_name =  models.CharField(max_length=64, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    def fill_from_form(self, cd):
        self.name = cd["name"]
        self.full_name = cd["full_name"] 
        self.details = cd["details"]

class Conference(models.Model):
    name = models.CharField(max_length=64)
    serial = models.IntegerField(null=True, blank=True)
    long_name = models.TextField()
    rank_1 = models.CharField(max_length=10, null=True, blank=True, choices=RANK_ALPHA)
    rank_2 = models.CharField(max_length=10, null=True, blank=True, choices=RANK_NUM)
    rank_3 = models.CharField(max_length=10, null=True, blank=True, choices=RANK_NUM)
    rank_4 = models.CharField(max_length=10, null=True, blank=True, choices=RANK_NUM)
    # category = models.CharField(max_length=64, null=True, blank=True)
    category = models.ForeignKey(ConferenceCategory, null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    is_favorite = models.BooleanField()
    deadline = models.DateField(null=True, blank=True)
    acceptance_rate = models.CharField(max_length=10, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    def fill_from_form(self, cd):
        self.name = cd["name"]
        self.serial = cd["serial"] 
        self.long_name = cd["long_name"]
        self.rank_1 = cd["rank_1"]       
        self.rank_2 = cd["rank_2"]       
        self.rank_3 = cd["rank_3"]       
        self.rank_4 = cd["rank_4"]       
        self.category = ConferenceCategory(id=cd["category"])
        self.website = cd["website"]       
        self.location = cd["location"]
        if 'is_favorite' in cd:
            self.is_favorite = True
        else:
            self.is_favorite = False
        if len(cd["deadline"]) > 0:       
            self.deadline = cd["deadline"]
        else:            
            self.deadline = None  
        self.acceptance_rate = cd["acceptance_rate"]       
        self.comment = cd["comment"]

    class Meta:
        ordering = ["name"]

class Publication(models.Model):
    name = models.CharField(max_length=64)
    serial = models.IntegerField()
    pub_type = models.CharField(max_length=16, choices=PUBLICATION_CHOICES)
    title = models.TextField()
    authors = models.TextField()
    journal = models.TextField()
    year = models.IntegerField()
    link = models.CharField(max_length=256, null=True, blank=True)
    pdf=models.CharField(max_length=256, null=True, blank=True)
    acceptance_rate = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=64, choices=PUBLICATION_STATUS_CHOICES, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    bibtex = models.TextField(null=True, blank=True)
    def converted_authors(self):
        authstr = self.authors.replace("and", " ")
        return authstr.replace(",", " AND ")
    def __unicode__(self):
        return self.name
    def fill_from_form(self, cd):
        self.name = cd["name"]
        self.serial = cd["serial"] 
        self.pub_type = cd["pub_type"]
        self.authors = cd["authors"]
        self.title = cd["title"]
        self.year = cd["year"]
        self.journal = cd["journal"]
        self.link = cd["link"]
        self.pdf = cd["pdf"]
        self.acceptance_rate = cd["acceptance_rate"]
        self.status = cd["status"]       
        self.comment = cd["comment"]
        self.bibtex = cd["bibtex"]
    class Meta:
        ordering = ["name"]

class AppContent(models.Model):
    name = models.CharField(max_length=64)
    caption = models.CharField(max_length=64)
    language = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    content = models.TextField()
    css = models.TextField(null=True, blank=True)
    js = models.TextField(null=True, blank=True)
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
            # self.content = db.Blob(file.read())
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
    class Meta:
        ordering = ["name"]
    
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
        # logging.info("#### %%%%%%%%%%%%%%%% SERVING FROM CACHE: :D")
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

def get_content_model_by_tile(tile):
    content = get_content_by_tile(tile)
    if content:
        return content, content.id
    else:
        return AppContent(), -1

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

def get_view(module_name, view_name):
    key = "%s-%s" % (module_name, view_name)
    data = cache.get(key)
    if data is not None:
        # logging.info("#### %%%%%%%%%%%%%%%% SERVING FROM CACHE")
        return data
    else:
        try:
            modules = AppModule.objects.filter(name=module_name)
            if modules:            
                appmodule = modules[0]
                views = AppView.objects.filter(module=appmodule, name=view_name)
                if views:
                    row = views[0]
                    cache.set(key, row, 3600)
                    return row
                else:
                    contents = AppContent.objects.filter(name=key)
                    if appmodule and contents:
                        content = contents[0]
                        row = AppView()
                        row.name = view_name
                        row.is_redirect = False
                        row.module = appmodule
                        row.default_content = content
                        return row
                    else:
                        return None
            else:
                logging.warn("Looking for Key: " + key)
                contents = AppContent.objects.filter(name=key)
                if contents:
                    content = contents[0]
                    dummy_module = AppModule()
                    row = AppView()
                    row.name = view_name
                    row.is_redirect = False
                    row.module = dummy_module
                    row.default_content = content
                    return row
                else:
                    return None
        except IndexError:
            return None

def get_view2(module, view):
    key = "%s-%s" % (module, view)
    data = cache.get(key)
#    data = None
    if data is not None:
        # logging.info("#### %%%%%%%%%%%%%%%% SERVING FROM CACHE: :D")
        return data
    else:
        try:
            appmodule = AppModule.objects.filter(name=module)[0]
            row = AppView.objects.filter(module=appmodule, name=view)[0]
            # logging.info(row)
            if row:
                cache.set(key, row, 3600)
                return row
            else:
                return None
        except IndexError:
            return None
