import unittest
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.core.urlresolvers import reverse

from . import views
from . import models


class PostTest(TestCase):
    def setUp(self):
        """본 테스트에 공통으로 사용하는 데이터들.
        test users를 만들고 이 이용자가 접근한다는 전제로 사용함.
        """
        self.client = Client()

    def _add_post_by_http(self, **kwargs):
        follow = kwargs.pop('follow', True)
        # 글 게시 시도.
        return self.client.post(
            '/blogtest/posts/create/', kwargs, follow=follow
        )

    def _add_category_by_model(self):
        category = models.Category(name='cat cat cat')
        category.save()
        return category

    def test_create_post_by_model(self):
        """모델을 이용해 게시물을 추가하는 테스트
        """
        category = self._add_category_by_model()
        post = models.Post(
            category=category,
            title='첫 번째 글!',
            content='Lorem Ipsum'
        )
        post.save()
        self.assertIsNotNone(post.pk)

        expected_post = models.Post.objects.latest('pk')
        self.assertEqual(post.pk, expected_post.pk)

    def test_create_many_post__by_model(self):
        """모델을 이용해 사진 데이터를 여러 번 추가하는 테스트
        """
        for i in range(30):
            category = self._add_category_by_model()
            post = models.Post(
                category=category,
                title='{}번 글!'.format(i),
                content='Lorem Ipsum'
            )
            post.save()
            self.assertIsNotNone(post.pk)

            expected_post = models.Post.objects.latest('pk')
            self.assertEqual(post.pk, expected_post.pk)

    def test_404(self):
        """없는 페이지에 접근하는 테스트.
        """
        response = self.client.get('/asdfasdfasdf/page_not_found/')
        self.assertEqual(response.status_code, 404)

    def test_create_post_by_view(self):
        """뷰 함수를 이용해 글을 게시하는 테스트.
        """
        # 카테고리 없이 글 게시 시도.
        response = self._add_post_by_http(
            title='hello world',
            content='Lorem Ipsum',
        )

        # 카테고리가 없고 이에 대한 예외 처리가 없으므로 404, 500 서버 에러.
        self.assertIn(response.status_code, (404, 500,))

        category = self._add_category_by_model()
        response = self._add_post_by_http(
            category=category.pk,
            title='hello world',
            content='Lorem Ipsum',
        )

        # 카테고리를 지정했으므로 정상 저장.
        self.assertEqual(response.status_code, 200)

    def test_list_post(self):
        """글 목록이 의도대로 동작하는지 테스트.
        """
        category = self._add_category_by_model()
        expected_count = 5
        for i in range(expected_count):
            response = self._add_post_by_http(
                category=category.pk,
                title='hello world {}'.format(i),
                content='Lorem Ipsum'
            )
            self.assertEqual(response.status_code, 200)

        posts = models.Post.objects.all()
        # 글 목록 페이지 접근.
        response = self.client.get('/blogtest/posts/', follow=True)
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # 이동한 URL의 뷰 함수가 list_post 인지 테스트.
        self.assertEqual(response.resolver_match.func, views.list_posts)
        # 템플릿 컨텍스트에 posts가 있는지 확인.
        self.assertIn('posts', response.context)
        # 템플릿 변수 posts의 데이터 개수 가져오기.
        res_count = response.context['posts'].count()
        # 그 개수가 expected_count인지 확인.
        self.assertEqual(res_count, expected_count)
        # 모델로 가져온 데이터 개수와 같은지 비교.
        self.assertEqual(posts.count(), res_count)

    def test_view_post(self):
        """개별 글 페이지가 의도대로 동작하는지 테스트.
        """
        # 존재하지 않는 사진에 접근.
        response = self.client.get('/blogtest/posts/1/', follow=True)
        # http status가 404인지 확인.
        self.assertEqual(response.status_code, 404)

        category = self._add_category_by_model()
        response = self._add_post_by_http(
            category=category.pk,
            title='hello world {}',
            content='Lorem Ipsum'
        )
        self.assertEqual(response.status_code, 200)

        # 게시한 글의 보기 URL 접근.
        response = self.client.get('/blogtest/posts/1/', follow=True)
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # 이동한 URL의 뷰 함수가 view_post 인지 테스트.
        self.assertEqual(response.resolver_match.func, views.view_post)
        # 템플릿 컨텍스트에 post가 있는지 확인.
        self.assertIn('post', response.context)
        # 그 photo의 pk가 1인지 확인.
        self.assertEqual(response.context['post'].pk, 1)
