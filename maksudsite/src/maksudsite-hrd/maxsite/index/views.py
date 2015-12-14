from maxsite.helper import response_from_db_or_default


def index(request):
    return response_from_db_or_default(request=request, module="home", view="index", pagename="Home", active_key="default")

def search(request):
    if request.method == "POST":
        if request.POST.get('search'):
            print request.POST.get('search')
            pass
    elif reqest.method == "GET":
        if request.GET.get('search'):
            print request.GET.get('search')
            pass
    return response_from_db_or_default(request, "home", "search", "Search", "default")

def module_index(request, module):
    return response_from_db_or_default(request=request, module=module, view="index", pagename=module, active_key="default")

def module_view_index(request, module, view):
    return response_from_db_or_default(request=request, module=module, view=view, pagename=module, active_key="default")
