import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Post


def create_post(user, title, image, text):
    return Post.objects.create(user=user, title=title, image=image, text=text)


# class PostModelTests(TestCase):
#
#     def test_text_longer_than_1500(self):
#         """
#         max length for text field is 1500
#         """
#
#         long_post = create_post(user=1, title='title', image=None, text='a'*1501)
#         assert
#         # self.assertIs(future_question.was_published_recently(), False)
