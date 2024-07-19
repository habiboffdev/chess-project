import pytest
from django.conf import settings
from django.core.management import execute_from_command_line


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        pass  # You can add any setup code here if needed
