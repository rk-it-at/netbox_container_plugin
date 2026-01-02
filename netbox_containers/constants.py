from utilities.choices import ChoiceSet


class PodStatusChoices(ChoiceSet):
    key = 'Pod.status'
    CHOICES = [
        ("created", "Created", "grey"),
        ("running", "Running", "green"),
        ("stopped", "Stopped", "yellow"),
        ("exited",  "Exited",  "orange"),
        ("dead",    "Dead",    "red"),
    ]
    colors = {v: c for v, _, c in CHOICES}

class NetworkDriverChoices(ChoiceSet):
    key = 'Network.driver'
    CHOICES = [
        ("bridge", "Bridge"),
        ("macvlan", "macvlan"),
        ("ipvlan", "ipvlan"),
    ]

class ImageArchChoices(ChoiceSet):
    key = "ImageTag.arch"
    CHOICES = [
        ("amd64",  "amd64"),
        ("arm64",  "arm64"),
        ("armv7",  "arm/v7"),
        ("s390x",  "s390x"),
        ("ppc64le","ppc64le"),
        ("riscv64","riscv64"),
    ]

class ImageOSChoices(ChoiceSet):
    key = "ImageTag.os"
    CHOICES = [
        ("linux",   "Linux"),
        ("windows", "Windows"),
    ]

class VolumeDriverChoices(ChoiceSet):
    key = 'Volume.driver'
    CHOICES = [
        ("local", "local"),
        ("image", "image"),
    ]