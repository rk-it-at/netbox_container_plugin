from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.rendering import FieldSet
from netbox_containers.models import Secret, SecretDriverChoices


__all__ = (
    "SecretForm",
    "SecretFilterForm",
    "SecretBulkEditForm",
)


class SecretForm(NetBoxModelForm):
    options = forms.CharField(
        required=False,
        label="Options",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One option per line.",
    )

    class Meta:
        model = Secret
        fields = [
            "name",
            "driver",
            "options",
            "tags",
        ]

    fieldsets = (
        FieldSet(
            "name",
            "driver",
            "options",
            "tags",
            name=_("Secret"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["options"] = self.instance.options or ""


class SecretBulkEditForm(NetBoxModelBulkEditForm):
    model = Secret

    driver = forms.ChoiceField(
        choices=SecretDriverChoices.choices,
        required=False,
        label=_("Driver"),
    )

    fieldsets = (
        FieldSet(
            "driver",
            name=_("Secret"),
        ),
    )


class SecretFilterForm(NetBoxModelFilterSetForm):
    model = Secret

    q = forms.CharField(required=False, label="Search")
    driver = forms.ChoiceField(
        choices=SecretDriverChoices.choices,
        required=False,
        label=_("Driver"),
    )

    fieldsets = (
        FieldSet("q", "driver", name=_("Secrets")),
    )
