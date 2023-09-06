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
    # Create test user
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a test list
    list_obj = List.objects.create(user=user, date='2023-09-05', important_event=True)

    # Create a test task associated with the list
    task = Task.objects.create(
        list=list_obj,
        title='Sample Task',
        description='This is a test task',
    )

    return user, list_obj, task


# LIST TESTS
@pytest.mark.django_db
def test_get_user_lists(create_test_data):
    # Unpacking data from fixture
    user, _, _ = create_test_data

    lists = get_user_lists(user=user)
    assert len(lists) == 1
    assert lists[0].user == user


@pytest.mark.django_db
def test_get_list_details(create_test_data):
    _, list_obj, _ = create_test_data

    list_details = get_list_details(list_id=list_obj.id)
    assert list_details.id == list_obj.id
    assert str(list_details.date) == '2023-09-05'
    assert list_details.important_event == True


@pytest.mark.django_db
def test_get_list_details_invalid_data():
    with pytest.raises(Http404):
        get_list_details(list_id=8888888)


@pytest.mark.django_db
def test_get_list_details_missing_data():
    with pytest.raises(Http404):
        get_list_details(None)


# TASKS TESTS
@pytest.mark.django_db
def test_get_list_tasks(create_test_data):
    _, list_obj, _ = create_test_data

    tasks = get_list_tasks(list_id=list_obj.id)
    assert len(tasks) == 1
    assert tasks[0].title == 'Sample Task'


@pytest.mark.django_db
def test_get_task_details(create_test_data):
    _, _, task = create_test_data

    task_details = get_task_details(task_id=task.id)
    assert task_details.id == task.id
    assert task_details.description == 'This is a test task'


@pytest.mark.django_db
def test_get_task_details_invalid_data():
    with pytest.raises(Http404):
        get_task_details(task_id=888888)


@pytest.mark.django_db
def test_get_task_details_missing_task():
    with pytest.raises(Http404):
        get_task_details(task_id=None)


# TEST PERMISSIONS

@pytest.mark.django_db
def test_if_anonymous_user_post_list_returns_403():
    client = APIClient()
    url_pattern_name = 'create_list'
    data = {
        'date': '2023-09-05',
        'important_event': False
    }

    response = client.post(reverse(url_pattern_name), data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_if_anonymous_user_post_task_returns_403():
    client = APIClient()

    url_pattern_name = 'create_task'

    data = {
        'title': 'New task',
        'description': 'Description',
        'tag': 'Work'
    }

    response = client.post(reverse(url_pattern_name, kwargs={'list_id': 1}), data=data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
