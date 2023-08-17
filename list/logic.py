from .models import Task, List


def get_user_lists(user):
    lists = List.objects.filter(user=user)
    return lists


def put_user_list(user):
    new_list = List.objects.update_or_create(user=user)
