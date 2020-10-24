import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

USER = get_user_model()


@pytest.mark.django_db
def test_user_create():
    USER.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert USER.objects.count() == 1


@pytest.mark.django_db
def test_view(client):
    url = reverse('users')
    response = client.get(url)
    assert response.status_code == 200
