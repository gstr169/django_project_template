from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '8080')
max_requests = 1000
worker_class = 'gevent'
workers = environ.get('WORKERS')
if workers == '':
    workers = max_workers()
else:
    workers = int(workers)
timeout = 300

env = {
    'DJANGO_SETTINGS_MODULE': 'configs.settings'
}


# TODO: change project name
reload = True
name = 'project'
