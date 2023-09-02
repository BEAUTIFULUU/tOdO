import pytest
from rest_framework.test import APIClient
from rest_framework import status
from list.models import List, Task


class TestListCreate:
    def test_if_anonymous_user_posts_data_returns_403(self):
        client = APIClient()
        response = client.post('/lists/', {'date': '31-08-2023',
                                           'important_event': 'false'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_if_authenticated_user_post_data_returns_201(self):
        client = APIClient()
        response = client.post('/lists/', {'date': '31-08-2023',
                                           'important_event': 'false'})

        assert List.objects.count() + 1
