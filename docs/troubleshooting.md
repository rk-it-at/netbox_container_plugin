# Troubleshooting

## UI changes are not visible

- Hard refresh browser cache.
- Restart NetBox services after code updates.
- Confirm updated plugin files are actually deployed.

## Migration errors

- Ensure plugin is enabled in `PLUGINS`.
- Run:

  ```bash
  python /opt/netbox/netbox/manage.py showmigrations netbox_containers
  python /opt/netbox/netbox/manage.py migrate netbox_containers
  ```

## Form field validation issues

Common formats:

- Published port: `8080:80`
- Env: `KEY=value`
- Add host: `hostname:ip`
- Add device: `/dev/ttyUSB0` or `/dev/sda:/dev/xvda:rwm`

## 500 errors after plugin update

- Check NetBox logs for traceback.
- Verify model changes have matching migrations.
- Verify serializer/table/template updates for newly added fields.

## Reporting an issue

Open a GitHub issue using the bug template and include:

- NetBox version
- Plugin version/commit
- Exact reproduction steps
- Full traceback
