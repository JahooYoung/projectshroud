from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from os import environ

from backend.models import Event

if environ.get('DJANGO_DB') == 'mysql':
    @register(Event)
    class EventIndex(AlgoliaIndex):
        fields = ('id', 'title', 'description')
        settings = {'searchableAttributes': ['title', 'description']}
        index_name = 'event_index'