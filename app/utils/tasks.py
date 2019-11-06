from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.timezone import localtime
from django.core.management import call_command

from utils.cache_locks import cache_lock

logger = get_task_logger(__name__)


@shared_task(bind=True)
def backup_task(self, apps_names: tuple = tuple()):
    with cache_lock('backup_all_lock', self.app.oid, 60 * 60) as acquired:
        if acquired:
            now = localtime()
            if len(apps_names):
                backup_filename = 'backup_' + str(now.date().isoformat()) + '.json'
            else:
                backup_filename = 'full_backup.json'
            call_command('dumpdata', *apps_names, '--indent', '4', '-o', f'/code/fixtures/{backup_filename}')
            logger.info('Backup completed at: ' + str(now.isoformat(sep=' ', timespec='seconds')))
        else:
            logger.info('MESSAGE: Backup already creating by another worker.')
