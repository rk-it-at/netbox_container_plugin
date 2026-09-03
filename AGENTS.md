# AGENTS.md

Guidance for AI coding agents (and humans) working on `netbox_container_plugin`. This
file describes what the project is, how it's structured, and the conventions its
maintainer (René Koch, rkoch@rk-it.at) expects contributions to follow.

## What this is

A [NetBox](https://github.com/netbox-community/netbox) plugin that documents container
infrastructure (Podman/Docker-style) as first-class NetBox objects: Containers, Pods,
Networks, Images/Image Tags, Volumes, Mounts, Secrets, Container Secrets, and Network
Attachments.

- PyPI package: `netbox-containers` (import path: `netbox_containers`)
- **Status: pre-1.0, alpha, not production-ready.** Breaking changes can happen between
  releases.
- Supports NetBox 4.4.x–4.6.x (see `min_version`/`max_version` in
  `netbox_containers/__init__.py`), Python 3.12+.
- This project is explicitly AI-assisted (see the "AI-Assisted Project" section of
  `README.md`) — substantial LLM-authored code with human review is the norm here, not an
  exception to flag.

## Repo map

```
netbox_containers/
  __init__.py            PluginConfig (version, min/max NetBox version, base_url)
  constants.py            All ChoiceSet definitions (status/driver/arch/os choices)
  navigation.py            PluginMenu / PluginMenuItem / PluginMenuButton (left nav)
  urls.py                  URL wiring, built via get_model_urls() per model + a few
                           custom "add from parent" routes
  models/                 One file per model (containers.py, pods.py, networks.py,
                           images.py, volumes.py, mounts.py, secrets.py,
                           container_secrets.py, network_attachments.py), all
                           re-exported via models/__init__.py (star imports)
  views/                  Same one-file-per-model split, generic.* based
  forms/                  Same split: <Model>Form, <Model>FilterForm,
                           <Model>BulkEditForm, plus ad-hoc *CreateForm/*EditForm for
                           "add from parent" flows
  tables/                 django_tables2 / NetBoxTable per model
  filtersets/              django_filters / NetBoxModelFilterSet per model
  templates/netbox_containers/   Hand-written detail templates (extend
                           generic/object.html) + a couple of *_children.html that just
                           extend generic/object_children.html
  templatetags/           netbox_containers_helpers.py — currently just render_boolean
  api/                    DRF serializers/views/urls, one ModelViewSet per model
  migrations/             Standard Django migrations
  tests/                  Django TestCase-based tests (currently model-level only)
docs/                      MkDocs end-user docs (see mkdocs.yml for nav)
changelogs/                 antsibull-changelog fragments + generated CHANGELOG.md
.github/workflows/          validate.yml (CI), release.yml (manual release),
                           docs-pages.yml (docs deploy)
```

`models/__init__.py`, `views/__init__.py`, `forms/__init__.py`, `tables/__init__.py`,
`filtersets/__init__.py`, `api/serializers/__init__.py` are all pure `from .x import *`
aggregators (each submodule declares `__all__`). This is a deliberate, accepted pattern
in this repo — the resulting `F403` ruff warnings are known and not something to "fix" by
collapsing files together.

## Architecture conventions

- Every model extends `netbox.models.NetBoxModel` and defines `get_absolute_url()`
  pointing at `plugins:netbox_containers:<lowercase_model_name>`.
- Status/driver/arch/os enums live centrally in `constants.py` as `ChoiceSet` subclasses
  (NetBox's `utilities.choices.ChoiceSet`), each with a `key` and `CHOICES`
  (value, label, [color]) — not scattered `TextChoices` per model, **except** a few
  smaller enums (`MountTypeChoices`, `ContainerSecretTypeChoices`,
  `NetworkAttachmentModeChoices`, `SecretDriverChoices`) that live next to their model
  instead of in `constants.py`. Follow whichever convention the field you're touching
  already uses.
- Views are built almost entirely from `netbox.views.generic` (`ObjectView`,
  `ObjectListView`, `ObjectEditView`, `ObjectDeleteView`, `BulkEditView`,
  `BulkDeleteView`, `ObjectChildrenView`) and registered via
  `utilities.views.register_model_view`. Don't hand-roll Django CBVs where a generic
  NetBox view already covers the case.
- "Child object added from a parent's detail page" (adding a Mount/ContainerSecret/
  NetworkAttachment directly from a Container or Pod page) is handled by dedicated
  `*CreateView`/`*CreateForm` classes wired as plain (non-`register_model_view`) URL
  patterns in `urls.py`, e.g. `containers/<int:container_id>/mounts/add/`. These views
  extract the parent id from `resolver_match` kwargs (with GET-param and regex-on-path
  fallbacks) and inject it into the form/instance.
- `urls.py` builds the per-model URL includes via a small `get_urls(model_name,
  url_prefix)` helper wrapping `utilities.urls.get_model_urls`. Add new models by adding
  one line here, not by writing `path()` entries by hand.
- Detail templates extend `generic/object.html` and build panels as hand-written
  Bootstrap `card`/`row`/`col` markup rather than NetBox's higher-level panel/table
  helpers. `*_children.html` templates for tab views just extend
  `generic/object_children.html` with no overrides — keep that minimal pattern for new
  child tabs.
- `templatetags/netbox_containers_helpers.py` currently defines `render_boolean`; check
  whether NetBox core's own `render_boolean` (`utilities/templatetags/builtins/filters.py`,
  loaded via `{% load helpers %}`) can be used instead before adding more custom filters —
  don't reimplement something NetBox core already provides.

### Data model (high level)

- `Container` → `Pod` (FK, nullable), `Container` → `ImageTag` (FK, nullable)
- `Pod.infra_container` → `Container` (FK, nullable; must be `is_infra=True` and belong to
  the pod)
- `NetworkAttachment` → exactly one of `Container` or `Pod`, plus either a `Network` FK
  (mode=`network`) or free-form `options` (mode=`custom`), or nothing (mode=`none`/
  `host`/`private`) — validated in both the model's `clean()` and the relevant form's
  `clean()`
- `Mount` → `Container` (FK) + either a `Volume` FK (mount_type=`volume`) or a
  `host_path` string (mount_type=`bind`) — same dual model+form validation pattern
- `ContainerSecret` → `Container` + `Secret`, `type` is `mount` or `env`; uid/gid/mode
  only valid for `mount`
- `Network`/`Container`/`Pod` all have `devices`/`virtual_machines` M2M to
  `dcim.Device`/`virtualization.VirtualMachine`; `Network` also M2M to `ipam.Prefix`
- Several fields (`environment`, `add_host`, `add_group`, `add_device` on `Container`;
  `add_host` on `Pod`) are stored as `JSONField(default=list)` but edited as newline-
  separated text via a paired `<field>_text` form field with a `clean_<field>_text`
  validator and a form-level `save()` override that copies the parsed list back onto the
  model field.

## Dev workflow

No Makefile/tox — everything is plain `pip`/`manage.py`/CLI tools.

```bash
# editable install into your NetBox venv
pip install -e /path/to/netbox_container_plugin

# add "netbox_containers" to PLUGINS in NetBox's configuration.py, then:
python /opt/netbox/netbox/manage.py migrate netbox_containers

# restart NetBox after every change if testing against a remote/deployed instance
```

Run the plugin's own tests with Django's test runner from inside a NetBox install (there's
no standalone test settings module in this repo):

```bash
python manage.py test netbox_containers
```

### Linting (must pass before pushing — mirrors CI)

```bash
python -m compileall .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
ruff check .
ruff format --diff .
```

CI (`validate.yml`) also runs a non-blocking `flake8 --exit-zero --max-complexity=10
--max-line-length=88` pass — worth glancing at even though it can't fail the build.

## Changelog fragments — required for every non-trivial PR

- Branches are named `<issue-number>-<kebab-summary>` (e.g.
  `23-feature-add-coding-agent-guidelines`).
- Every PR needs a fragment at `changelogs/fragments/<branch-name>.yml`, matching the
  branch name exactly. Example:
  ```yaml
  ---
  minor_changes:
    - "[Feature]: Short description (https://github.com/rk-it-at/netbox_container_plugin/issues/<n>)"
  ...
  ```
  Valid top-level keys (see `changelogs/config.yaml`): `major_changes`, `minor_changes`,
  `breaking_changes`, `deprecated_features`, `removed_features`, `security_fixes`,
  `bugfixes`, `known_issues`.
- CI (`validate.yml` → `changelog` job) fails the build if the fragment is missing
  (skipped only when building the default branch itself), and separately runs
  `antsibull-changelog lint`.
- Fragments are consumed by the (manual, `workflow_dispatch`) `release.yml` workflow,
  which bumps `__version__` in `netbox_containers/__init__.py` and `version` in
  `pyproject.toml`, runs `antsibull-changelog release`, opens a `release/vX.Y.Z` PR, tags,
  and publishes a GitHub release with built artifacts. Don't hand-edit `CHANGELOG.md`
  directly — it's generated.

## Documentation

End-user docs live in `docs/` and are built with MkDocs (`readthedocs` theme, nav defined
in `mkdocs.yml`) and auto-deployed to GitHub Pages on push to `main`
(`.github/workflows/docs-pages.yml`). If you add a page, add it to `mkdocs.yml`'s `nav`
too.

## Coding guidelines (from CONTRIBUTING.md)

- Keep changes focused; open an issue first for larger design changes.
- Update templates/forms/tables/serializers/filtersets together when adding a model
  field — this codebase's one-file-per-concern-per-model layout means a new field
  typically touches 5–6 files.
- Include or update tests when behavior changes.
- Include the generated migration when models change.
- Keep compatibility with the NetBox version range declared in `README.md` /
  `netbox_containers/__init__.py`.
