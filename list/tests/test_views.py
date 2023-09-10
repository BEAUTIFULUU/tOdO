import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from list.models import List, Task


User = get_user_model()


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def create_list(create_user):
    user = create_user
    list_obj = List.objects.create(user=user, date='2023-09-05', important_task=True)
    return list_obj


@pytest.fixture
def create_task(create_list):
    list_obj = create_list
    task = Task.objects.create(
        list=list_obj, is_completed=True, title='Sample Task', description='This is a test task', tag='Home')
    return task


def make_authenticated_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()
    client.login(username=username, password=password)
    return user, client


@pytest.mark.django_db
class TestListViews:

    def test_list_view_return_lists_for_authenticated_user(self):
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = reverse('get_create_list')
        response = client.get(url_pattern)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data.get('results'), list)

    def test_list_view_creates_list_for_authenticated_user(self):
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = reverse('get_create_list')
        data = {
            'date': '2023-09-10',
            'important_task': False,
        }
        response = client.post(url_pattern, data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert List.objects.filter(user=user).count() == 1

    def test_list_detail_view_update_list_for_authenticated_user(self, create_list):
        list_obj = create_list
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_list'
        data = {
            'date': '2023-11-11',
            'Important task': True
        }

        response = client.put(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')
        updated_list = List.objects.get(id=list_obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert str(updated_list.date) == '2023-11-11'
        assert updated_list.important_task is True

    def test_list_detail_view_delete_list_for_authenticated_user(self, create_list):
        list_obj = create_list
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_list'
        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id}))

        assert List.objects.filter(user=user).count() == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestTaskViews:
    def test_task_view_return_tasks_for_authenticated_user(self, create_list):
        list_obj = create_list
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        response = client.get(reverse(url_pattern, kwargs={'list_id': list_obj.id}))

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data.get('results'), list)

    def test_task_view_create_task_for_authenticated_user(self, create_list):
        list_obj = create_list
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        data = {
            'is_completed': True,
            'title': 'title',
            'description': 'description',
            'tag': 'Work'
        }
        response = client.post(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.filter(list_id=list_obj).count() == 1

    def test_task_detail_view_update_task_for_authenticated_user(self, create_list, create_task):
        list_obj = create_list
        task_obj = create_task
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        data = {
            'is_completed': False,
            'title': '111',
            'description': '222',
            'tag': 'Work'
        }

        response = client.put(
            reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task_obj.id}), data=data, format='json')
        updated_task = Task.objects.get(list_id=list_obj.id, id=task_obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert updated_task.is_completed is False
        assert updated_task.title == '111'
        assert updated_task.description == '222'
        assert updated_task.tag == 'Work'

    def test_task_detail_view_delete_task_for_authenticated_user(self, create_list, create_task):
        list_obj = create_list
        task_obj = create_task
        user, client = make_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task_obj.id}))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.filter(list_id=list_obj.id).count() == 0
