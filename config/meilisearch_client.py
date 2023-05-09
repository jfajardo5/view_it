import meilisearch
from django.conf import settings

meilisearch_client = meilisearch.Client(settings.MEILISEARCH_HOST)
