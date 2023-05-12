from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Videos
from .tasks import add_user_to_search_index, add_video_to_search_index

User = get_user_model()


# Receiver for Users' post_save signal
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    A signal that adds an user to the search index when created.
    """
    # Check if the user was just created
    if created:
        # Add it to the search index asynchronously
        transaction.on_commit(lambda: add_user_to_search_index.delay(user_id=instance.id))


# Receiver for Videos' post_save signal
@receiver(post_save, sender=Videos)
def video_created(sender, instance, created, **kwargs):
    """
    A signal that creates a thumbnail from the video file and adds the video to the search index
    when a new video is saved.
    """
    # Check if the video was just created
    if created:
        # If the video is public, add it to the search index asynchronously
        if instance.status == "public":
            transaction.on_commit(lambda: add_video_to_search_index.delay(video_id=instance.id))
