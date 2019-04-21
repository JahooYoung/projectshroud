from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from backend.models import Event

@register(Event)
class EventIndex(AlgoliaIndex):
    fields = ('id', 'title', 'description')
    settings = {'searchableAttributes': ['title', 'description']}
    index_name = 'event_index'