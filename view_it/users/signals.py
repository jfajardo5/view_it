from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from view_it.search.tasks import add_user_to_search_index

User = get_user_model()


# Receiver for the post_save signal
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    A signal that adds an user to the search index when created.
    """
    # Check if the user was just created
    if created:
        # Add it to the search index asynchronously
        transaction.on_commit(lambda: add_user_to_search_index.delay(instance.id))
