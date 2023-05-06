from collections.abc import Sequence
from typing import Any

import factory
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from view_it.users.tests.factories import UserFactory
from view_it.videos.models import Videos


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Videos
        django_get_or_create = ["url_slug"]

    title = Faker("sentence", nb_words=5)
    description = Faker("paragraph", nb_sentences=5)
    user = factory.SubFactory(UserFactory)
    url_slug = Faker("uuid4")

    @post_generation
    def file(self, create: bool, extracted: Sequence[Any], **kwargs):
        file = (
            extracted
            if extracted
            else Faker(
                "file_name",
                category="video",
                extension=".mp4",
            ).evaluate(None, None, extra={"locale": None})
        )
        self.file = file

    @post_generation
    def thumbnail(self, create: bool, extracted: Sequence[Any], **kwargs):
        thumbnail = (
            extracted
            if extracted
            else Faker(
                "file_name",
                category="image",
                extension=".png",
            ).evaluate(None, None, extra={"locale": None})
        )
        self.thumbnail = thumbnail

    @post_generation
    def status(self, create: bool, extracted: Sequence[Any], **kwargs):
        status = extracted if extracted else "public"
        self.status = status
