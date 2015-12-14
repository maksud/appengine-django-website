
from apps import search
from apps.search.core import porter_stemmer
from maxsite.models import AppContent

search.register(AppContent, ('content','caption', ),    indexer=porter_stemmer)