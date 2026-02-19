# NetBox Containers Plugin

Plugin to document containers, pods, networks, volume mounts and secrets in NetBox.

**Status:** This plugin is under active development and is **not** recommended for production use yet!

It will support Podman and Docker - other container engines aren't supported, by may work if they use the same logic and Podman and Docker.

## Features
- Containers with mounts, network attachments, secrets, infra flag, devices/VMs, tags, and comments
- Pods with infra container, network attachments, add-host, devices/VMs, tags, and comments
- Networks with attachments to containers/pods and IPAM integration
- Images and image tags
- Volumes and mounts
- Secrets (driver + options)

## Requirements
- NetBox 4.4.x–4.5.x
- Python 3.12 (or newer)

## Installation (dev)
1. Install in your NetBox venv:
   ```bash
   pip install -e /path/to/netbox_container_plugin
   ```
2. Add to `PLUGINS` in `configuration.py`:
   ```python
   PLUGINS = [
       "netbox_containers",
   ]
   ```
3. Run migrations:
   ```bash
   python /opt/netbox/netbox/manage.py migrate netbox_containers
   ```
4. Restart NetBox.

## Usage
- Containers: add mounts, networks, and secrets via “Add Components” on the container detail page.
- Pods: add network attachments via “Add Components” on the pod detail page.
- Network attachments support both “User defined network” and custom modes (none/host/private/custom).
- Secrets can be attached to containers with type (mount/env), target, and optional uid/gid/mode.

## Data Model (high level)
- `Container` ↔ `Pod` (FK)
- `NetworkAttachment` connects a `Container` or `Pod` to a `Network` or custom options
- `Mount` belongs to a `Container`
- `ContainerSecret` attaches a `Secret` to a `Container`
- `Secret` has name, driver, options (text)

## Development notes
- Migrations live in `netbox_containers/migrations/`
- If you’re copying files to a remote NetBox server, restart NetBox after each change.
- See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution workflow, required changelog fragments, and PR expectations.

## License
See [`LICENSE`](LICENSE).
