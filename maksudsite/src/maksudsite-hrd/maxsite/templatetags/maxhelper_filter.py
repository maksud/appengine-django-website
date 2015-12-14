from django import template
from django.template.defaultfilters import stringfilter
from maxsite.models import get_content_string_by_tile
import datetime
import hashlib


register = template.Library()


@register.filter
@stringfilter
def md5(value):
    return hashlib.md5(value).hexdigest()

@register.simple_tag
def contents_tile(tile_id):
    content, content_id = get_content_string_by_tile(str(tile_id))
    return content

@register.simple_tag
def contents_tile_mv(module, view):
    return contents_tile(str(module)+"-"+str(view))

@register.simple_tag
def contents_tile_mvc(module, view, content):
    return contents_tile(str(module)+"-"+str(view)+"-"+str(content))

@register.simple_tag
def current_time(format_string):
    format_string = str(format_string)
    return datetime.datetime.now().strftime(format_string)

