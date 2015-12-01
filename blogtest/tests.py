from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client
from django.conf import settings

from . import views
from . import models


class PostTest(TestCase):
    def setUp(self):
        """본 테스트에 공통으로 사용하는 데이터들.
        test users를 만들고 이 이용자가 접근한다는 전제로 사용함.
        """
        self.client = Client()
        user_model = get_user_model()
        self.user1 = user_model.objects \
            .create_user(username='test1', password='1')
        self.user2 = user_model.objects \
            .create_user(username='test2', password='2')

    def test_create_post_by_model(self):
        """모델을 이용해 게시물을 추가하는 테스트
        """
        category = self._add_category_by_model()
        post = models.Post(
            user=self.user1,
            category=category,
            title='첫 번째 글!',
            content='Lorem Ipsum'
        )
        post.save()
        self.assertIsNotNone(post.pk)

        expected_post = models.Post.objects.latest('pk')
        self.assertEqual(post.pk, expected_post.pk)

    def test_create_many_post_by_model(self):
        """모델을 이용해 사진 데이터를 여러 번 추가하는 테스트
        """
        for i in range(30):
            category = self._add_category_by_model()
            post = models.Post(
                user=self.user1,
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

    def test_create_post_without_auth_by_view(self):
        """로그인해야만 글쓰기 화면과 게시 가능한 지 테스트
        """
        self._logout()
        response = self.client.get('/blogtest/posts/create/', follow=True)
        # 로그인 하지 않았으므로 로그인 URL로 redirect 됐는지 확인.
        self.assertEqual(response.resolver_match.func.__name__, 'login')
        self.assertEqual(response.redirect_chain[0][1], 302)

        category = self._add_category_by_model()
        response = self._add_post_by_http(
            category=category.pk,
            title='hello world {}',
            content='Lorem Ipsum'
        )
        # 로그인 하지 않았으므로 로그인 URL로 redirect 됐는지 확인.
        self.assertEqual(response.resolver_match.func.__name__, 'login')
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_create_post_with_form_by_view(self):
        """Form validator에 걸려서 글쓰기 화면이 그대로 나오는 테스트
        """
        # 1번 이용자로 로그인
        user = self.user1
        self._login(user.pk)
        category = self._add_category_by_model()

        # 카테고리만 넣고 글 게시 시도.
        response = self._add_post_by_http(
            category=category.pk,
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # view_post 뷰 함수로 이동하지 않고 글 작성
        self.assertEqual(response.resolver_match.func, views.create_post)
        # 템플릿 변수 form에 title, content 필드 오류가 존재하는지?
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('title'))
        self.assertTrue(response.context['form'].has_error('content'))

        # 글 본문을 빼고 게시 시도
        response = self._add_post_by_http(
            title='hello',
            category=category.pk,
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # view_post 뷰 함수로 이동하지 않고 글 작성
        self.assertEqual(response.resolver_match.func, views.create_post)
        # 템플릿 변수 form에 title, content 필드 오류가 존재하는지?
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('content'))

        # 글 제목을 빼고 게시 시도
        response = self._add_post_by_http(
            content='hello',
            category=category.pk,
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # view_post 뷰 함수로 이동하지 않고 글 작성
        self.assertEqual(response.resolver_match.func, views.create_post)
        # 템플릿 변수 form에 title, content 필드 오류가 존재하는지?
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('title'))

        # 게시 시도
        expected_title = 'ASDFESDFasdfkasjdf;klsajdflk32kljsdafsad'
        response = self._add_post_by_http(
            title=expected_title,
            content='world',
            category=category.pk,
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # view_post 뷰 함수로 이동하지 않고 글 작성
        self.assertEqual(response.resolver_match.func, views.view_post)
        # 템플릿 변수 form에 title, content 필드 오류가 존재하는지?
        ctx = response.context
        self.assertIn('post', ctx)
        self.assertEqual(ctx['post'].title, expected_title)
        self.assertEqual(ctx['post'].user.pk, user.pk)

    def test_create_post_by_view(self):
        """뷰 함수를 이용해 글을 게시하는 테스트.
        """
        # 1번 이용자로 로그인
        user = self.user1
        self._login(user.pk)

        # 카테고리 없이 글 게시 시도.
        response = self._add_post_by_http(
            title='hello world',
            content='Lorem Ipsum',
        )

        # 카테고리가 없어서 글 편집 화면으로 돌아오므로 200 status이고 create_post 뷰함수
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.create_post)

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
        # 1번 이용자로 로그인
        user = self.user1
        self._login(user.pk)

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
        # 1번 이용자로 로그인
        user = self.user1
        self._login(user.pk)

        # 존재하지 않는 사진에 접근.
        response = self.client.get('/blogtest/posts/111111/', follow=True)
        # http status가 404인지 확인.
        self.assertEqual(response.status_code, 404)

        category = self._add_category_by_model()
        response = self._add_post_by_http(
            category=category.pk,
            title='hello world {}',
            content='Lorem Ipsum'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('post', response.context)
        self.assertIsNotNone(response.context['post'].pk)
        saved_post_pk = response.context['post'].pk

        # 게시한 글의 보기 URL 접근.
        response = self.client.get(
            '/blogtest/posts/{}/'.format(saved_post_pk), follow=True
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # 이동한 URL의 뷰 함수가 view_post 인지 테스트.
        self.assertEqual(response.resolver_match.func, views.view_post)
        # 템플릿 컨텍스트에 post가 있는지 확인.
        self.assertIn('post', response.context)
        # 그 photo의 pk가 1인지 확인.
        self.assertEqual(response.context['post'].pk, saved_post_pk)

    def test_delete_post(self):
        """게시한 글 삭제하기 테스트
        """
        # 1번 이용자로 로그인
        self._login(self.user1.pk)

        category = self._add_category_by_model()
        response = self._add_post_by_http(
            category=category.pk,
            title='hello world {}',
            content='Lorem Ipsum'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('post', response.context)
        self.assertIsNotNone(response.context['post'].pk)
        saved_post_pk = response.context['post'].pk

        # 게시한 글의 보기 URL 접근.
        response = self.client.get(
            '/blogtest/posts/{}/'.format(saved_post_pk), follow=True
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)
        # 이동한 URL의 뷰 함수가 view_post 인지 테스트.
        self.assertEqual(response.resolver_match.func, views.view_post)

        # 다른 이용자로 로그인
        self._logout()
        self._login(self.user2.pk)
        # 다른 이용자로 글 삭제 시도.
        response = self.client.post(
            '/blogtest/posts/{}/delete/'.format(saved_post_pk),
            follow=True
        )
        # 다른 이용자가 게시한 글을 지우려 한 것이므로 403이나 500 응답
        self.assertIn(response.status_code, (403, 500))
        # 글이 여전히 남아있는지 확인.
        response = self.client.get(
            '/blogtest/posts/{}/'.format(saved_post_pk), follow=True
        )
        # http status code가 200인지 확인.
        self.assertEqual(response.status_code, 200)

        # 다른 이용자로 로그인
        self._logout()
        self._login(self.user1.pk)
        # 다른 이용자로 글 삭제 시도.
        response = self.client.post(
            '/blogtest/posts/{}/delete/'.format(saved_post_pk),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # 이동한 URL의 뷰 함수가 view_post 인지 테스트.
        self.assertEqual(response.resolver_match.func, views.list_posts)

        # 글이 남아있지 않으므로 404 status
        response = self.client.get(
            '/blogtest/posts/{}/'.format(saved_post_pk), follow=True
        )
        self.assertEqual(response.status_code, 404)

    def _add_post_by_http(self, **kwargs):
        """글 작성하는 편의용 메서드.
        """
        follow = kwargs.pop('follow', True)
        # 글 게시 시도.
        return self.client.post(
            '/blogtest/posts/create/', kwargs, follow=follow
        )

    def _add_category_by_model(self):
        """모델로 직접 카테고리 추가하는 편의용 메서드.
        """
        category = models.Category(name='cat cat cat')
        category.save()
        return category

    def _login(self, user_number):
        num = str(user_number)
        # 로그인 시도.
        return self.client.post(
            settings.LOGIN_URL, {
                'username': 'test{}'.format(num),
                'password': num
            }
        )

    def _logout(self):
        return self.client.get(settings.LOGOUT_URL)
