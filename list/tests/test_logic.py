import pytest
from django.contrib.auth import get_user_model
from django.http import Http404
from django.urls import reverse
from list.models import List, Task
from list.logic import get_user_lists, get_list_details, get_list_tasks, get_task_details
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def create_authenticated_user():
    def make_authenticated_user(username, password):
        user = User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        return user, client

    return make_authenticated_user


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


@pytest.mark.django_db
class TestListLogic:
    def test_get_user_lists(self, create_user, create_list):
        user = create_user

        lists = get_user_lists(user=user)
        assert len(lists) == 1
        assert user in [list.user for list in lists]

    def test_get_list_details(self, create_list):
        list_obj = create_list

        list_details = get_list_details(list_id=list_obj.id)
        assert list_details.id == list_obj.id
        assert str(list_details.date) == '2023-09-05'
        assert list_details.important_task is True

    def test_get_list_details_invalid_data(self):
        with pytest.raises(Http404):
            get_list_details(list_id=8888888)

    def test_get_list_details_missing_data(self):
        with pytest.raises(Http404):
            get_list_details(None)


@pytest.mark.django_db
class TestTaskLogic:
    def test_get_list_tasks(self, create_list, create_task):
        list_obj = create_list

        tasks = get_list_tasks(list_id=list_obj.id)
        assert len(tasks) == 1
        found_task = None
        for task in tasks:
            if task.title == 'Sample Task':
                found_task = task
                break
        assert found_task is not None

    def test_get_task_details(self, create_task):
        task = create_task

        task_details = get_task_details(task_id=task.id)
        assert task_details.id == task.id
        assert task_details.description == 'This is a test task'

    def test_get_task_details_invalid_data(self):
        with pytest.raises(Http404):
            get_task_details(task_id=888888)

    def test_get_task_details_missing_task(self):
        with pytest.raises(Http404):
            get_task_details(task_id=None)


@pytest.mark.django_db
class TestListPermissionsLogic:

    def test_if_authenticated_user_get_lists_returns_200(self, create_authenticated_user):
        user, client = create_authenticated_user(username='testuser', password='testpassword')
        url_pattern = 'get_create_list'
        response = client.get(reverse(url_pattern))

        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_create_list_returns_201(self, create_authenticated_user):
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_list'
        data = {
            'date': '2023-09-05',
            'important_task': True
        }

        response = client.post(reverse(url_pattern), data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_authenticated_user_update_list_returns_200(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_list'
        data = {
            'date': '2023-10-09',
            'important_task': False
        }

        response = client.put(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_delete_list_returns_204(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_list'

        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_anonymous_user_get_lists_returns_403(self):
        client = APIClient()
        url_pattern = 'get_create_list'
        response = client.get(reverse(url_pattern))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_create_list_returns_403(self):
        client = APIClient()
        url_pattern = 'get_create_list'
        data = {
            'date': '2023-09-05',
            'important_task': False
        }

        response = client.post(reverse(url_pattern), data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_update_list_returns_403(self, create_list):
        list_obj = create_list
        client = APIClient()
        url_pattern = 'update_delete_list'
        data = {
            'date': '2023-09-06',
            'important_task': False
        }

        response = client.put(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_delete_list_returns_403(self, create_list):
        list_obj = create_list
        client = APIClient()
        url_pattern = 'update_delete_list'
        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTaskPermissionsLogic:

    def test_if_authenticated_user_get_tasks_returns_200(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        response = client.get(reverse(url_pattern, kwargs={'list_id': list_obj.id}))

        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_create_task_returns_201(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        data = {
            'is_completed': True,
            'title': 'title',
            'description': 'description',
            'tag': 'Work'
        }

        response = client.post(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_authenticated_user_update_task_returns_200(self, create_authenticated_user, create_list, create_task):
        list_obj = create_list
        task = create_task
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        data = {
            'is_completed': False,
            'title': 'title1',
            'description': 'description1',
            'tag': 'Home'
        }

        response = client.put(
            reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}), data=data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_delete_task_returns_204(self, create_authenticated_user, create_list, create_task):
        list_obj = create_list
        task = create_task
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_anonymous_user_get_tasks_returns_403(self, create_list):
        list_obj = create_list
        client = APIClient()
        url_pattern = 'get_create_task'
        response = client.get(reverse(url_pattern, kwargs={'list_id': list_obj.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_create_task_returns_403(self):
        client = APIClient()
        url_pattern = 'get_create_task'

        data = {
            'is_completed': False,
            'title': 'New task',
            'description': 'Description',
            'tag': 'Work'
        }

        response = client.post(reverse(url_pattern, kwargs={'list_id': 1}), data=data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_update_task_returns_403(self, create_list, create_task):
        list_obj = create_list
        task = create_task
        client = APIClient()
        url_pattern = 'update_delete_task'
        data = {
            'is_completed': True,
            'title': 'Old Task',
            'description': 'Second Description',
            'tag': 'Sport'
        }

        response = client.put(reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}), data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_delete_task_returns_403(self, create_list, create_task):
        list_obj = create_list
        task = create_task
        client = APIClient()
        url_pattern = 'update_delete_task'

        response = client.delete(reverse(url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}))
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTaskInvalidData:
    def test_create_task_with_no_title_returns_400(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        data = {
            'is_completed': True,
            'description': 'description',
            'tag': 'Home'
        }

        response = client.post(
            reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_with_no_description_returns_400(self, create_authenticated_user, create_list):
        list_obj = create_list
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'get_create_task'
        data = {
            'is_completed': True,
            'title': 'title',
            'tag': 'Home'
        }

        response = client.post(reverse(url_pattern, kwargs={'list_id': list_obj.id}), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_task_with_no_title_returns_404(self, create_authenticated_user, create_list, create_task):
        list_obj = create_list
        task = create_task
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        data = {
            'is_completed': True,
            'description': 'description',
            'tag': 'Home'
        }

        response = client.put(reverse(
            url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_task_with_no_description_returns_404(self, create_authenticated_user, create_list, create_task):
        list_obj = create_list
        task = create_task
        user, client = create_authenticated_user(username='123', password='123')
        url_pattern = 'update_delete_task'
        data = {
            'is_completed': True,
            'title': 'title',
            'tag': 'Home'
        }

        response = client.put(reverse(
            url_pattern, kwargs={'list_id': list_obj.id, 'task_id': task.id}), data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def create_users():
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')
    return user1, user2


@pytest.fixture
def create_authenticated_client(create_users):
    user, _ = create_users
    client = APIClient()
    client.force_authenticate(user=user)
    return client




