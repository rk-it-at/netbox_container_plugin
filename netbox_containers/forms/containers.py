from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Container, Pod, Network, Image, ImageTag


__all__ = (
    "ContainerForm",
    "ContainerFilterForm",
    "ContainerBulkEditForm",
)


class ContainerForm(NetBoxModelForm):
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks",
    )
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )
    comments = CommentField(required=False)
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Devices",
    )
    virtual_machines = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual machines",
    )
    image = DynamicModelChoiceField(
        queryset=Image.objects.all(),
        required=False,
        label="Image",
        help_text="Select repository/image first",
    )
    image_tag = DynamicModelChoiceField(
#        queryset=ImageTag.objects.none(),
        queryset=ImageTag.objects.select_related("image"),
        required=False,
        label="Tag",
        help_text="Select tag (filtered by image)",
        query_params={
            "image_id": "$image",
        },
    )

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "pod",
            "image",
            "image_tag",
            "devices",
            "virtual_machines",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image_tag"].queryset = ImageTag.objects.none()

        # Editing existing container → prepopulate
        if self.instance.pk and self.instance.image_tag:
            self.fields['image'].initial = self.instance.image_tag.image
            self.fields['image_tag'].queryset = ImageTag.objects.filter(
                image=self.instance.image_tag.image
            )

        # Image selected (POST)
        if 'image' in self.data:
            try:
                image_id = int(self.data.get('image'))
                self.fields['image_tag'].queryset = ImageTag.objects.filter(image_id=image_id)
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.image_tag_id:
            self.fields["image_tag"].queryset = ImageTag.objects.filter(image=self.instance.image_tag.image)


    def clean(self):
        super().clean()

        image = self.cleaned_data.get('image')
        image_tag = self.cleaned_data.get('image_tag')

        if image_tag and image and image_tag.image != image:
            raise forms.ValidationError("Selected tag does not belong to selected image.")

        return self.cleaned_data


class ContainerBulkEditForm(NetBoxModelBulkEditForm):
    model = Container

    user = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "user",
            name=_("Pod"),
        ),
    )

    nullable_fields = ("user", "comments")  


class ContainerFilterForm(NetBoxModelFilterSetForm):
    model = Container

    q = forms.CharField(required=False, label="Search")

    status = forms.ChoiceField(
        choices=Container._meta.get_field("status").choices,
        required=False,
        label=_("Status"),
    )
    user   = forms.CharField(required=False, label="User")

    # Filter Containers by related Networks
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks"
    )
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )

    fieldsets = (
        FieldSet("q", "status", "user", "networks", "pod", name=_("Containers")),
    )
