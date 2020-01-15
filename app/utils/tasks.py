from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.timezone import localtime
from django.core.management import call_command

from utils.cache_locks import cache_lock
from utils.apps import *

logger = get_task_logger(__name__)


@shared_task()
def backup_task(apps_labels: tuple = tuple()):
    with cache_lock('_backup_lock', timeout=3600) as acquired:
        if acquired:
            now = localtime()
            if not apps_labels:
                apps_labels = get_apps_labels()
                apps_labels = tuple(filter(lambda x: x not in ('contenttypes', 'auth', 'sessions'), apps_labels))
            apps_labels = (*apps_labels, 'auth.user', 'auth.group')
            backup_filename = 'backup_' + str(now.date().isoformat()) + '.json'
            call_command('dumpdata', *apps_labels, '--natural-foreign', '--indent', '4', '-o',
                         f'/code/fixtures/{backup_filename}')
            logger.info('Backup completed at: ' + str(now.isoformat(sep=' ', timespec='seconds')))
        else:
            logger.info('MESSAGE: Backup already creating by another worker.')
