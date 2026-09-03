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
  views/                  Same one-file-per-model split, generic.* based, plus
                           mixins.py (ParentLookupMixin for "add from parent"
                           *CreateView classes; RelatedDeviceVMTablesMixin for
                           the Devices/VMs render_table sub-tables)
  forms/                  Same split: <Model>Form, <Model>FilterForm,
                           <Model>BulkEditForm, plus ad-hoc *CreateForm/*EditForm for
                           "add from parent" flows, plus fields.py (shared
                           LineListField and its regexes)
  tables/                 django_tables2 / NetBoxTable per model
  filtersets/              django_filters / NetBoxModelFilterSet per model
  templates/netbox_containers/   Detail templates (extend generic/object.html),
                           delegating Tags/Comments to NetBox's own
                           inc/panels/*.html includes, + a couple of
                           *_children.html that just extend generic/object_children.html
  templatetags/           empty (init only) — no plugin-specific tags/filters
                           needed; see "Use NetBox's own includes/tags" below
  api/                    DRF serializers/views/urls, one ModelViewSet per model
  migrations/             Standard Django migrations
  tests/                  Django TestCase-based tests (currently model-level only)
docs/                      MkDocs end-user docs (see mkdocs.yml for nav)
changelogs/                 antsibull-changelog fragments + generated CHANGELOG.md
.github/workflows/          validate.yml (CI), release.yml (manual release),
                           docs-pages.yml (docs deploy)
.yamllint                   yamllint config (extends "default", strict)
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
  mix in `views.mixins.ParentLookupMixin` and call its `_get_parent_id(request,
  kwarg_name, path_regex, get_param_names=())` to resolve the parent id (kwargs →
  resolver_match → GET param → regex-on-path fallback), each exposing a thin
  `_get_container_id`/`_get_pod_id` wrapper for readability at call sites. Add new
  "add from parent" views on top of this mixin rather than re-copying the lookup chain.
- `urls.py` builds the per-model URL includes via a small `get_urls(model_name,
  url_prefix)` helper wrapping `utilities.urls.get_model_urls`. Add new models by adding
  one line here, not by writing `path()` entries by hand.
- Cross-field validation (e.g. "exactly one of container/pod", "uid/gid/mode only valid
  for mount secrets") lives on the **model's** `clean()`, not on individual forms.
  `ModelForm._post_clean()` calls `instance.full_clean()` automatically, so every form
  for that model gets the same validation for free — including "add from parent" forms
  that exclude the parent FK from `Meta.fields`, since the parent id is already set on
  the instance (via the view's `get_object()`) before validation runs. Don't re-add a
  `clean()` override to a form to duplicate a check the model already makes.
- "One entry per line" text fields (`add_host_text`, `environment_text`, etc. — backed
  by a model `JSONField(default=list)`) use `forms.fields.LineListField`, a
  `forms.Field` that parses/validates newline-separated input into a list and renders a
  list value back as text via `prepare_value`. Add a new such field with
  `LineListField(line_regex=..., line_error="...")` rather than writing another
  `clean_<field>_text` method by hand.
- Detail templates extend `generic/object.html` and still build the object's own
  field-attribute panel as hand-written Bootstrap `card`/`row`/`col` markup — NetBox
  core does the same thing in its own templates (there's no generic "auto panel" for
  a model's own fields; core apps hand-write an `attr-table` for that too). `*_children.html`
  templates for tab views just extend `generic/object_children.html` with no
  overrides — keep that minimal pattern for new child tabs. **When copying a detail
  template for a new model, delete panels for relations the new model doesn't
  actually have** (e.g. a copy-pasted "Devices"/"Virtual Machines"/"Pods" panel
  referencing `object.devices`/`object.pods` on a model with no such field silently
  renders as "No devices associated." forever — Django swallows the missing-attribute
  lookup instead of erroring, so this kind of dead panel won't surface itself; grep the
  model before trusting a copied template).
- **Use NetBox's own includes/tags instead of hand-rolling these** (verified against
  NetBox core v4.4–v4.6 source):
  - Tags panel → `{% include 'inc/panels/tags.html' %}` (needs `object` in context,
    which every detail template already has). Renders each tag via NetBox's own
    `{% tag %}` builtin, which respects the tag's actual assigned color — a hand-rolled
    `text-bg-primary` pill hardcodes one color for every tag regardless of what's set.
  - Comments panel → `{% include 'inc/panels/comments.html' %}`. Renders
    `object.comments` through NetBox's `markdown` filter — a hand-rolled `<div
    style="white-space:pre-wrap;">` shows plain text only, silently dropping any
    Markdown formatting `CommentField` is meant to support.
  - Boolean check/X icon (e.g. `is_infra`) → `{% checkmark object.is_infra %}`, a
    Django template **builtin** (`utilities.templatetags.builtins.tags`, registered in
    NetBox's `TEMPLATES` `OPTIONS.builtins`) — no `{% load %}` needed, available in
    every template automatically.
  - Every related-object sub-table on a detail page (Devices/VMs on Container/Pod/
    Network; Mounts/Secrets/Networks on Container; Containers/Networks on Pod;
    Pods/Containers on Network) is a real table instance —
    `dcim.tables.DeviceTable`, `virtualization.tables.VirtualMachineTable`, or one of
    this plugin's own `tables.py` classes (`MountTable`, `ContainerSecretTable`,
    `NetworkAttachmentTable`, `ContainerTable`, `PodTable`) — built in the view's
    `get_extra_context()` and rendered via `{% load render_table from django_tables2 %}`
    and `{% render_table sometable %}`, the same mechanism NetBox core uses for an
    inline related-object table (e.g. `dcim/virtualdevicecontext.html`). This gets correct
    status colors, linkification, sorting and column choice for free instead of a
    hand-rolled `<table>`. Rules of thumb when adding one:
    - **Prefix every table instance** (`DeviceTable(qs, prefix="devices-")`) so its
      sort/pagination query params don't collide with another table on the same page —
      `RelatedDeviceVMTablesMixin.get_device_vm_tables()` in `views/mixins.py` already
      does this for Devices/VMs; do the same for any new one.
    - **Hide the column that just points back at the page you're on** (e.g.
      `containers_table.columns.hide("pod")` on a Pod's own Containers panel,
      `networks_table.columns.hide("container")` + `.hide("pod")` on a
      Container's/Pod's own Networks panel) — self-referential columns add nothing.
      `pk` (bulk-select) also gets hidden for `DeviceTable`/`VirtualMachineTable`
      specifically, since these are inline snippets without a bulk-action form; the
      plugin's own tables don't default-show `pk` so no extra hide is needed for them.
    - **If the table has a `LinkedCountColumn` in `default_columns`** (`ContainerTable`'s
      `device_count`/`vm_count`, `PodTable`'s `container_count`/`device_count`/
      `vm_count`) — those columns read an annotation (e.g. `Count("devices",
      distinct=True)`) that only exists if you put it on the queryset yourself; the
      table's own `get_queryset()` method is dead code (never called outside its own
      `*ListView`, which already annotates independently) — don't rely on it, replicate
      the `.annotate(...)` calls from the matching `*ListView.queryset` when building the
      table elsewhere (see `PodView`/`NetworkView.get_extra_context()`).
  - For any *other* status field you display outside a NetBoxTable-based table (i.e.
    you can't use `ChoiceFieldColumn`), the equivalent inline markup is `<span
    class="badge text-bg-{{ obj.get_status_color }}">{{ obj.get_status_display
    }}</span>` — `get_status_color()` follows the same `get_<field>_color()`
    convention this plugin's own `Container`/`Pod` use, and returns one of NetBox's
    extended palette names (`green`/`cyan`/`red`/`purple`/`yellow`/`gray`, not plain
    Bootstrap semantic names) — don't hand-roll an if/elif status→color chain.
  - NetBox core has no `render_boolean` filter (`checkmark` above is the real native
    equivalent) and no generic "panel" tag for arbitrary related-object tables beyond
    tags/comments/custom_fields — `django_tables2`'s `render_table` (above) is the
    closest thing, and requires an actual `Table` instance from the view.

### Data model (high level)

- `Container` → `Pod` (FK, nullable), `Container` → `ImageTag` (FK, nullable)
- `Pod.infra_container` → `Container` (FK, nullable; must be `is_infra=True` and belong to
  the pod)
- `NetworkAttachment` → exactly one of `Container` or `Pod`, plus either a `Network` FK
  (mode=`network`) or free-form `options` (mode=`custom`), or nothing (mode=`none`/
  `host`/`private`) — validated once, in the model's `clean()` (see the cross-field
  validation note above)
- `Mount` → `Container` (FK) + either a `Volume` FK (mount_type=`volume`) or a
  `host_path` string (mount_type=`bind`) — same model-only validation pattern
- `ContainerSecret` → `Container` + `Secret`, `type` is `mount` or `env`; uid/gid/mode
  only valid for `mount` (validated on the model, same as above)
- `Network`/`Container`/`Pod` all have `devices`/`virtual_machines` M2M to
  `dcim.Device`/`virtualization.VirtualMachine`; `Network` also M2M to `ipam.Prefix`.
  `Image`/`Volume` do **not** — see the template note above about not copy-pasting those
  panels onto models without the relation.
- Several fields (`environment`, `add_host`, `add_group`, `add_device` on `Container`;
  `add_host` on `Pod`) are stored as `JSONField(default=list)` but edited as newline-
  separated text via a paired `<field>_text` `LineListField` and a form-level `save()`
  override that copies the parsed list back onto the model field.

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
yamllint .
```

CI (`validate.yml`) also runs a non-blocking `flake8 --exit-zero --max-complexity=10
--max-line-length=88` pass — worth glancing at even though it can't fail the build.

YAML files (workflows, issue templates, `mkdocs.yml`, `changelogs/config.yaml`, etc.) are
linted by `yamllint` against the repo's `.yamllint` config, which extends `default` and
turns nearly every optional rule on (2-space indentation enforced *inside* multi-line block
scalars too, `---`/`...` document markers required, no bare `on:`/`yes`/`no` truthy values,
no empty mapping values, 120-char line length). Two consequences worth knowing before editing
workflow YAML:

- Any multi-line `run: |` block must have **every line at the same indentation** as its
  first line — `check-multi-line-strings` is on, so the usual convention of indenting a
  shell `if`/`then` body an extra level, or continuation lines of a `\`-continued command,
  will fail lint. Flatten shell blocks to one indentation level (bash doesn't care).
- Where the embedded content *must* keep internal indentation to stay valid (e.g. the
  Python heredoc in `release.yml`'s "Bump version in project files" step), wrap it in
  `# yamllint disable rule:indentation` / `# yamllint enable rule:indentation` comments
  placed outside the block scalar, rather than fighting the rule or weakening the config.
- GitHub Actions' `on:` key must be quoted (`"on":`) — unquoted `on` is YAML 1.1 truthy
  syntax for `true`, which `yamllint`'s `truthy` rule flags.
- `changelogs/changelog.yaml` is excluded (`ignore:` in `.yamllint`) since antsibull-changelog
  generates it.

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
