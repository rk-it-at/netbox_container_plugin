from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "ImageView",
    "ImageListView",
    "ImageEditView",
    "ImageDeleteView",
    "ImageTagView",
    "ImageTagListView",
    "ImageTagEditView",
    "ImageTagDeleteView",
)


@register_model_view(models.Image)
class ImageView(generic.ObjectView):
    queryset = models.Image.objects.all()
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    template_name = "netbox_containers/image.html"
    form = forms.ImageForm


@register_model_view(models.Image, "list", path="", detail=False)
class ImageListView(generic.ObjectListView):
    queryset = models.Image.objects.all()
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    filterset_form = forms.ImageFilterForm


@register_model_view(models.Image, "add", detail=False)
@register_model_view(models.Image, "edit")
class ImageEditView(generic.ObjectEditView):
    queryset = models.Image.objects.all()
    form = forms.ImageForm


@register_model_view(models.Image, "delete")
class ImageDeleteView(generic.ObjectDeleteView):
    queryset = models.Image.objects.all()


@register_model_view(models.Image, "bulk_edit", path="bulk-edit", detail=False)
class ImageBulkEditView(generic.BulkEditView):
    queryset = models.Image.objects.all()
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    form = forms.ImageBulkEditForm


@register_model_view(models.Image, "bulk_delete", path="bulk-delete", detail=False)
class ImageBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Image.objects.all()
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet


@register_model_view(models.Image, "changelog", path="changelog")
class ImageChangeLogView(generic.ObjectChangeLogView):
    queryset = models.Image.objects.all()


@register_model_view(models.Image, "journal", path="journal")
class ImageJournalView(generic.ObjectJournalView):
    queryset = models.Image.objects.all()

# Image Tags

@register_model_view(models.ImageTag)
class ImageTagView(generic.ObjectView):
    queryset = models.ImageTag.objects.all()
    table = tables.ImageTagTable
    filterset = filtersets.ImageTagFilterSet
    template_name = "netbox_containers/image_tag.html"
    form = forms.ImageTagForm


@register_model_view(models.ImageTag, "list", path="", detail=False)
class ImageTagListView(generic.ObjectListView):
    queryset = models.ImageTag.objects.all()
    table = tables.ImageTagTable
    filterset = filtersets.ImageTagFilterSet
    filterset_form = forms.ImageTagFilterForm


@register_model_view(models.ImageTag, "add", detail=False)
@register_model_view(models.ImageTag, "edit")
class ImageTagEditView(generic.ObjectEditView):
    queryset = models.ImageTag.objects.all()
    form = forms.ImageTagForm


@register_model_view(models.ImageTag, "delete")
class ImageTagDeleteView(generic.ObjectDeleteView):
    queryset = models.ImageTag.objects.all()


#@register_model_view(models.ImageTag, "bulk_edit", path="bulk-edit", detail=False)
#class ImageTagBulkEditView(generic.BulkEditView):
#    queryset = models.ImageTag.objects.all()
#    table = tables.ImageTagTable
#    filterset = filtersets.ImageTagFilterSet
#    form = forms.ImageTagBulkEditForm
#
#
#@register_model_view(models.ImageTag, "bulk_delete", path="bulk-delete", detail=False)
#class ImageTagBulkDeleteView(generic.BulkDeleteView):
#    queryset = models.ImageTag.objects.all()
#    table = tables.ImageTagTable
#    filterset = filtersets.ImageTagFilterSet


@register_model_view(models.ImageTag, "changelog", path="changelog")
class ImageTagChangeLogView(generic.ObjectChangeLogView):
    queryset = models.ImageTag.objects.all()


@register_model_view(models.ImageTag, "journal", path="journal")
class ImageTagJournalView(generic.ObjectJournalView):
    queryset = models.ImageTag.objects.all()
