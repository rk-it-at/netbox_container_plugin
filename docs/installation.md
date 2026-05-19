# Installation

## Requirements

- NetBox 4.4.x or 4.5.x
- Python 3.12+
- Access to NetBox virtual environment

## Install plugin

```bash
pip install netbox-containers
```

## Enable plugin in NetBox

In NetBox `configuration.py`:

```python
PLUGINS = [
    "netbox_containers",
]
```

## Apply migrations

```bash
python /opt/netbox/netbox/manage.py migrate netbox_containers
```

## Restart NetBox services

Restart your NetBox services (for example `netbox` and `netbox-rq`).

## Validate installation

1. Open NetBox.
2. Confirm the plugin menu is visible.
3. Open each main list page once:
   - Containers
   - Pods
   - Infra -> Networks, Volumes, Secrets, Images, Image Tags

![Installation placeholder](images/installation-plugin-menu.png)

## Upgrade notes

When upgrading plugin code:

1. Update installed code/package.
2. Run migrations.
3. Restart services.
4. Hard-refresh browser cache if template or JS behavior changed.
