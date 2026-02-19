# NetBox Containers Plugin

[![Release](https://img.shields.io/github/v/release/rk-it-at/netbox_container_plugin)](https://github.com/rk-it-at/netbox_container_plugin/releases)
[![License](https://img.shields.io/github/license/rk-it-at/netbox_container_plugin)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/rk-it-at/netbox_container_plugin/validate.yml?branch=main&label=ci)](https://github.com/rk-it-at/netbox_container_plugin/actions/workflows/validate.yml)
[![Docs](https://img.shields.io/github/actions/workflow/status/rk-it-at/netbox_container_plugin/docs-pages.yml?branch=main&label=docs)](https://github.com/rk-it-at/netbox_container_plugin/actions/workflows/docs-pages.yml)
[![PyPI](https://img.shields.io/pypi/v/netbox-containers)](https://pypi.org/project/netbox-containers/)
[![Python](https://img.shields.io/pypi/pyversions/netbox-containers)](https://pypi.org/project/netbox-containers/)
[![NetBox](https://img.shields.io/badge/NetBox-4.4.x--4.5.x-blue)](#requirements)

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

## Documentation
- End-user documentation is available in [`docs/`](docs/README.md).
- GitHub Pages publishing guidance is in [`docs/github-pages.md`](docs/github-pages.md).

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
