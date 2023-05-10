from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from view_it.search.tasks import add_video_to_search_index
from view_it.videos.tasks import generate_thumbnail

from .models import Videos


# Receiver for the post_save signal
@receiver(post_save, sender=Videos)
def video_created(sender, instance, created, **kwargs):
    """
    A signal that creates a thumbnail from the video file and adds the video to the search index
    when a new video is saved.
    """

    # Check if the video was just created
    if created:
        # If the video doesn't have a thumbnail, create one asynchronously
        if not instance.thumbnail:
            transaction.on_commit(lambda: generate_thumbnail.delay(instance.id, instance.file.url))

        # If the video is public, add it to the search index asynchronously
        if instance.status == "public":
            transaction.on_commit(lambda: add_video_to_search_index.delay(instance.id))
