import django_tables2 as tables
from django.utils.html import format_html
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Image, ImageTag


__all__ = (
    "ImageTable",
    "ImageTagTable",
)


class ImageTable(NetBoxTable):
    registry = tables.Column(verbose_name="Registry")
    name = tables.Column(linkify=True, verbose_name="Name")
    default_tag = tables.Column(verbose_name="Default tag")
    tag_count = columns.LinkedCountColumn(
        accessor='tag_count',
        viewname='plugins:netbox_containers:tag_list',
        url_params={'images_id': 'pk'},
        verbose_name="Tags",
        orderable=False,
    )
    label = tables.Column(linkify=True,)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Image
        fields = (
            'pk',
            'name',
            'registry',
            'default_tag',
            "tag_count",
            "label",
            "tags"
        )
        default_columns = (
            'name', 'registry', 'default_tag', 'tag_count', 'label'
        )

#    def get_queryset(self, request):
#        qs = super().get_queryset(request)
#        return (
#            qs
#            .annotate(tag_count=Count("devices", distinct=True))
#        )


class ImageTagTable(NetBoxTable):
    image = tables.Column(linkify=True, verbose_name="Image")
    image_tag = tables.Column(verbose_name="Tag")

    # If your model fields use ChoiceSet for os/arch, ChoiceFieldColumn will render labels/badges nicely.
    os = columns.ChoiceFieldColumn(verbose_name="OS")
    arch = columns.ChoiceFieldColumn(verbose_name="Arch")

    # Show a short digest (sha256:…); keep full value in title
    digest = tables.Column(verbose_name="Digest", empty_values=())

    def render_digest(self, record: ImageTag):
        if not record.digest:
            return "—"
        short = record.digest
        if len(short) > 19:
            short = f"{record.digest[:12]}…{record.digest[-5:]}"
        return format_html('<span title="{}">{}</span>', record.digest, short)

    # Optional: human-ish size
    size = tables.Column(verbose_name="Size", empty_values=(), orderable=False)

    def render_size(self, record: ImageTag):
        b = record.size
        if not b:
            return "—"
        # lightweight humanize
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if b < 1024.0:
                return f"{b:.1f} {unit}"
            b /= 1024.0
        return f"{b:.1f} PB"

    tags = columns.TagColumn()  # NetBox-native tags on ImageTag

    class Meta(NetBoxTable.Meta):
        model = ImageTag
        fields = (
            "pk",
            "image",
            "image_tag",
            "os",
            "arch",
            "digest",
            "size",
            "tags",
        )
        default_columns = (
            "image",
            "image_tag",
            "os",
            "arch",
            "digest",
            "size",
        )
