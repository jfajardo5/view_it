import meilisearch
from django.conf import settings
from django.contrib.auth import get_user_model

from view_it.videos.models import Videos

User = get_user_model()


# The Search class handles operations related to MeiliSearch
class Search:
    # Initialize MeiliSearch client with provided host in settings
    def __init__(self):
        self.client = meilisearch.Client(settings.MEILISEARCH_HOST)

    # Get or create a search index. An index is where the documents are stored.
    def get_index(self, index_name):
        try:
            # Get all indexes
            indexes = self.client.get_indexes()
        except self.client.errors as errors:
            # Raise any errors
            raise errors

        # Look for the required index in the retrieved indexes
        for index in indexes["results"]:
            if index.uid == index_name:
                return index

        # If the index doesn't exist, create a new one
        self.client.create_index(index_name)
        index = self.client.index(index_name)

        # Update searchable attributes based on the index
        if index_name == "users":
            index.update_searchable_attributes(["username"])
        elif index_name == "videos":
            index.update_searchable_attributes(["title"])

        return index

    # Add a document to the index. A document is a record in MeiliSearch.
    def add_document_to_index(self, index_name, document):
        index = self.get_index(index_name=index_name)
        index.add_documents([document], "id")
        # Return the task. A task in MeiliSearch represents an asynchronous operation.
        return self.client.get_task(0)

    # Add a video to the 'videos' index
    def add_video(self, video_id: int):
        video = Videos.objects.get(id=video_id)

        # Prepare the document
        document = {
            "id": video.id,
            "url": str(video.get_absolute_url()),
            "title": video.title,
            "description": video.description,
            "user": video.user.username,
        }

        # Add the document to the 'videos' index
        return self.add_document_to_index(index_name="videos", document=document)

    # Add a user to the 'users' index
    def add_user(self, user_id: int):
        user = User.objects.get(id=user_id)

        # Prepare the document
        document = {
            "id": user.id,
            "username": user.username,
            "description": user.channel_description if user.channel_description else "",
            "avatar": user.avatar.url if user.avatar else "",
            "url": str(user.get_absolute_url()),
        }

        # Add the document to the 'users' index
        return self.add_document_to_index(index_name="users", document=document)
