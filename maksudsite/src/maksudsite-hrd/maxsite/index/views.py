from maxsite.helper import response_from_db_or_default


def index(request):
    return response_from_db_or_default(request, "home", "index", "Home", "default")

def search(request):
    if request.method == "POST":
        if request.POST.get('search'):
            print request.POST.get('search')
            pass
    return response_from_db_or_default(request, "home", "search", "Search", "default")

def module_index(request, module):
    return response_from_db_or_default(request, module, "index", module, "default")

def module_view_index(request, module, view):
    return response_from_db_or_default(request, module, view, module, "default")
