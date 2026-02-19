# Contributing

Thanks for contributing to `netbox_container_plugin`.

This project is in active development. Contributions are welcome for bug fixes, tests, docs, and new features that align with the existing scope (NetBox container documentation for Podman/Docker-like workflows).

## Before You Start

- Check open issues and existing PRs to avoid duplicate work.
- For larger changes, open an issue first and describe the design.
- Keep changes focused and small where possible.

## Development Setup

1. Fork and clone your fork.
2. Create a branch from `main`:
   ```bash
   git checkout -b <your-feature-branch>
   ```
3. Install locally (editable):
   ```bash
   pip install -e .
   ```
4. If you test against a NetBox instance, ensure the plugin is in `PLUGINS` and run migrations:
   ```bash
   python /opt/netbox/netbox/manage.py migrate netbox_containers
   ```

## Required for Every PR

### 1) Changelog fragment

A changelog fragment is required for non-trivial changes.

- File location: `changelogs/fragments/`
- File name: `<branch-name>.yml`
- Example:
  ```yaml
  ---
  bugfix:
    - "Fix mount form validation when attaching from container view."
  ...
  ```

CI validates that the fragment exists and runs `antsibull-changelog lint`.

### 2) Migrations (if model changes)

If you modify models, include the generated migration in
`netbox_containers/migrations/`.

### 3) Validation

Run these checks before pushing:

```bash
python -m compileall .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

If available in your environment, also run:

```bash
antsibull-changelog lint
```

## Coding Guidelines

- Follow current project structure and naming conventions.
- Keep compatibility with supported NetBox versions from `README.md`.
- Prefer explicit, maintainable code over clever shortcuts.
- Update templates/forms/tables/serializers together when adding fields.
- Include or update tests when behavior changes.

## Pull Request Guidelines

PRs should include:

- Clear summary of what changed and why
- Any migration notes
- UI/API impact notes (if relevant)
- Screenshots for UI changes (recommended)

Keep PRs reviewable; split unrelated work into separate PRs.

## Reporting Bugs

When opening a bug report, include:

- NetBox version
- Plugin version/commit
- Steps to reproduce
- Expected vs actual behavior
- Traceback/log output (if any)

## Release and Stability Note

This plugin is not production-ready yet. Breaking changes may happen between pre-1.0 releases.
