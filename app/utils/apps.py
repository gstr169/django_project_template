from django.apps.registry import apps


def get_apps_labels():
    """
    Get apps list and return tuple of apps labels.
    """
    return tuple(app.label for app in apps.get_app_configs())
