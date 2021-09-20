import random, string

from django.contrib.auth.hashers import make_password


def add_dummy_password(strategy, details, backend, user=None, *args, **kwargs):
    user.password = make_password(''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    user.save()

