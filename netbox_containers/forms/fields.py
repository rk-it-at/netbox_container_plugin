import re

from django import forms

__all__ = (
    "DEVICE_ENTRY_RE",
    "ENV_ENTRY_RE",
    "GROUP_ENTRY_RE",
    "HOST_ENTRY_RE",
    "LineListField",
)

HOST_ENTRY_RE = re.compile(r"^[^:\s]+:[^:\s]+$")  # hostname:ip (simple)
ENV_ENTRY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")  # KEY=VALUE
GROUP_ENTRY_RE = re.compile(r"^[^\s]+$")
DEVICE_ENTRY_RE = re.compile(r"^/[^\s]*$")


class LineListField(forms.Field):
    """A Textarea field that parses newline-separated entries into a list of strings.

    Blank lines are dropped. If `line_regex` is given, every remaining line must
    match it, or a ValidationError naming the offending entries is raised.
    Renders a model's existing list value back as newline-separated text.
    """

    widget = forms.Textarea

    def __init__(self, *, line_regex=None, line_error=None, **kwargs):
        kwargs.setdefault("required", False)
        self.line_regex = line_regex
        self.line_error = line_error or "Invalid entry. Bad entries: {bad}"
        super().__init__(**kwargs)

    def to_python(self, value):
        raw = (value or "").strip()
        if not raw:
            return []

        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if self.line_regex is not None:
            bad = [line for line in lines if not self.line_regex.match(line)]
            if bad:
                raise forms.ValidationError(
                    self.line_error.format(bad=", ".join(bad[:5]))
                )
        return lines

    def prepare_value(self, value):
        if isinstance(value, (list, tuple)):
            return "\n".join(value)
        return value
