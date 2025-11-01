from django.conf import settings


def get_plugin_config(key, default=None):
    """
    Safely read a config value from PLUGINS_CONFIG["netbox_containers"].
    """
    plugin_settings = settings.PLUGINS_CONFIG.get("netbox_containers", {})
    return plugin_settings.get(key, default)
