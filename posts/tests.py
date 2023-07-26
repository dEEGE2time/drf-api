from django.contrib.auth.models import User
from .models import Post
from rest_framework import  status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
    
    def test_logged_in_user_can_create_post(self):
        # login
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        # Create two users
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        # Create two posts
        Post.objects.create(
            owner=adam,
            title='a title',
            content='adams content'
        )
        Post.objects.create(
            owner=brian,
            title='another title',
            content='brians content'
        )
    
    def test_can_retrieve_post_using_valid_id(self):
        # get request to fetch 1st post
        response = self.client.get('/posts/1/')
        # match title
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cant_retrieve_post_using_invalid_id(self):
        # get request to fetch invalid post
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        # put(edit) request to url with their post id, update title for test
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetch post by ID (1)
        post = Post.objects.filter(pk=1).first()
        # test that title changed
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cant_update_other_post(self):
        self.client.login(username='brian', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)