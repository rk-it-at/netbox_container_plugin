from netbox.plugins import PluginConfig
from django.conf import settings

class ContainersConfig(PluginConfig):
    name = 'netbox_containers'
    verbose_name = 'NetBox Container'
    description = 'Manage Podman/Docker container in NetBox'
    min_version = "4.4.0"
    version = '0.1'
    base_url = 'netbox-containers'
    author = "René Koch"
    author_email = "rkoch@rk-it.at"

config = ContainersConfig