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

    title = Faker("sentence", nb_words=5)
    description = Faker("paragraph", nb_sentences=5)
    user = factory.SubFactory(UserFactory)

    @post_generation
    def status(self, create: bool, extracted: Sequence[Any], **kwargs):
        status = extracted if extracted else "public"
        self.status = status
