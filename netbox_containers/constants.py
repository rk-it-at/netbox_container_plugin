from typing import ClassVar

from utilities.choices import ChoiceSet


class PodStatusChoices(ChoiceSet):
    key = "Pod.status"
    CHOICES: ClassVar[list] = [
        ("created", "Created", "gray"),
        ("running", "Running", "green"),
        ("stopped", "Stopped", "yellow"),
        ("exited", "Exited", "orange"),
        ("dead", "Dead", "red"),
    ]
    colors: ClassVar[dict] = {v: c for v, _, c in CHOICES}


class ContainerStatusChoices(ChoiceSet):
    key = "Container.status"
    CHOICES: ClassVar[list] = [
        ("created", "Created", "gray"),
        ("initialized", "Initialized", "gray"),
        ("running", "Running", "green"),
        ("paused", "Paused", "yellow"),
        ("exited", "Exited", "orange"),
        ("unknown", "Unknown", "red"),
    ]
    colors: ClassVar[dict] = {v: c for v, _, c in CHOICES}


class NetworkDriverChoices(ChoiceSet):
    key = "Network.driver"
    CHOICES: ClassVar[list] = [
        ("bridge", "Bridge"),
        ("macvlan", "macvlan"),
        ("ipvlan", "ipvlan"),
    ]


class ImageArchChoices(ChoiceSet):
    key = "ImageTag.arch"
    CHOICES: ClassVar[list] = [
        ("amd64", "amd64"),
        ("arm64", "arm64"),
        ("armv7", "arm/v7"),
        ("s390x", "s390x"),
        ("ppc64le", "ppc64le"),
        ("riscv64", "riscv64"),
    ]


class ImageOSChoices(ChoiceSet):
    key = "ImageTag.os"
    CHOICES: ClassVar[list] = [
        ("linux", "Linux"),
        ("windows", "Windows"),
    ]


class VolumeDriverChoices(ChoiceSet):
    key = "Volume.driver"
    CHOICES: ClassVar[list] = [
        ("local", "local"),
        ("image", "image"),
    ]
