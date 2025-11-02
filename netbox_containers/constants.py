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
