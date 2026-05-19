from netbox.plugins import PluginConfig


__version__ = "0.2.0"
class ContainersConfig(PluginConfig):
    name = 'netbox_containers'
    verbose_name = 'NetBox Container'
    description = 'Netbox plugin to manage Podman/Docker container'
    min_version = "4.4.0"
    max_version = "4.6.99"
    version = __version__
    base_url = 'netbox-containers'
    author = "René Koch"
    author_email = "rkoch@rk-it.at"


config = ContainersConfig
