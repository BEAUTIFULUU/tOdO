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
def create_test_data():
    user = User.objects.create_user(username='testuser', password='testpassword')
    list_obj = List.objects.create(user=user, date='2023-09-05', important_task=True)
    task = Task.objects.create(
        list=list_obj, is_completed=True, title='Sample Task', description='This is a test task', tag='Home')
    return user, list_obj, task


@pytest.mark.django_db
class TestListLogic:
    def test_get_user_lists(self, create_test_data):
        user, _, _ = create_test_data

        lists = get_user_lists(user=user)
        assert len(lists) == 1
        assert lists[0].user == user

    def test_get_list_details(self, create_test_data):
        _, list_obj, _ = create_test_data

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


# TASKS TESTS
@pytest.mark.django_db
class TestTaskLogic:
    def test_get_list_tasks(self, create_test_data):
        _, list_obj, _ = create_test_data

        tasks = get_list_tasks(list_id=list_obj.id)
        assert len(tasks) == 1
        found_task = None
        for task in tasks:
            if task.title == 'Sample Task':
                found_task = task
                break
        assert found_task is not None

    def test_get_task_details(self, create_test_data):
        _, _, task = create_test_data

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
    def test_if_anonymous_user_post_list_returns_403(self):
        client = APIClient()
        url_pattern_name = 'create_list'
        data = {
            'date': '2023-09-05',
            'important_task': False
        }

        response = client.post(reverse(url_pattern_name), data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_update_list_returns_403(self, create_test_data):
        _, list_obj, _ = create_test_data
        client = APIClient()
        list_id = list_obj.id
        url_pattern_name = 'update_delete_list'
        data = {
            'date': '2023-09-06',
            'important_task': False
        }

        response = client.put(reverse(url_pattern_name, kwargs={'list_id': list_id}), data=data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_delete_list_returns_403(self, create_test_data):
        _, list_obj, _ = create_test_data
        client = APIClient()
        list_id = list_obj.id
        url_pattern_name = 'update_delete_list'
        response = client.delete(reverse(url_pattern_name, kwargs={'list_id': list_id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    class TestTaskPermissionsLogic:
        def test_if_anonymous_user_post_task_returns_403(self):
            client = APIClient()
            url_pattern_name = 'create_task'

            data = {
                'is_completed': False,
                'title': 'New task',
                'description': 'Description',
                'tag': 'Work'
            }

            response = client.post(reverse(url_pattern_name, kwargs={'list_id': 1}), data=data, format='json')

            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_anonymous_user_update_task_returns_403(self, create_test_data):
            _, list_obj, task = create_test_data
            task_id = task.id
            list_id = list_obj.id
            client = APIClient()
            url_pattern_name = 'update_delete_task'
            data = {
                'is_completed': True,
                'title': 'Old Task',
                'description': 'Second Description',
                'tag': 'Sport'
            }

            response = client.put(reverse(url_pattern_name, kwargs={'list_id': list_id, 'task_id': task_id}), data=data)
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_anonymous_user_delete_task_returns_403(self, create_test_data):
            _, list_obj, task = create_test_data
            client = APIClient()
            task_id = task.id
            list_id = list_obj.id
            url_pattern_name = 'update_delete_task'

            response = client.delete(reverse(url_pattern_name, kwargs={'list_id': list_id, 'task_id': task_id}))
            assert response.status_code == status.HTTP_403_FORBIDDEN


