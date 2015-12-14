from django.http import HttpResponse
from maxsite.statichelper import get_static_content
import datetime

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

def output_content(content, serve=True):
    response = HttpResponse()
    response['Content-Type'] = content.content_type
    last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
    response['Last-Modified'] = last_modified
    response['ETag'] = content.etag
    if serve:
#        print content.body
        response.write(content.body)
#        response.out.write(content.body)
        return response
    else:
        response.status = 304
        return response

def content(request, name):
    data = get_static_content(name)
    if not data:
#        self.error(404)
        return HttpResponse(status=404)

    serve = True
    if 'If-Modified-Since' in request.META:
        last_seen = datetime.datetime.strptime(
            request.META['If-Modified-Since'],
            HTTP_DATE_FMT)
        if last_seen >= data.last_modified.replace(microsecond=0):
            serve = False
    if 'If-None-Match' in request.META:
        etags = [x.strip() for x in request.META['If-None-Match'].split(',')]
        if data.etag in etags:
            serve = False
    return output_content(data, serve)
