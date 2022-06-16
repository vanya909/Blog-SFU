from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from posts.utils import get_all_groups_sfu
from users.models import StudyGroup


class Command(BaseCommand):
    help = 'Creates all groups'

    def handle(self, *args, **kwargs):
        groups_list = get_all_groups_sfu()
        for group in groups_list:
            StudyGroup.objects.create(title=group)
            self.stdout.write(self.style.SUCCESS('Successfully create group "%s"' % group))
        self.stdout.write(self.style.SUCCESS('Successfully create all groups'))
