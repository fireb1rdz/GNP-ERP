# apps/logistics/forms.py
from django import forms
from apps.entities.models import Party


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleCTEFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return [single_file_clean(data, initial)]

class MultipleNFEFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return [single_file_clean(data, initial)]

class ConferenceCreateForm(forms.Form):
    CREATION_MODE_CHOICES = (
        ("cte", "Via CT-e"),
        ("nfe", "Via NF-e"),
        ("access_key", "Chave de Acesso"),
    )

    creation_mode = forms.ChoiceField(
        choices=CREATION_MODE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )

    cte_files = MultipleCTEFileField(required=False)

    nfe_files = MultipleNFEFileField(required=False)

    access_keys = forms.CharField(
        max_length=9999,
        required=False,
    )

    supplier = forms.ModelChoiceField(
        queryset=Party.objects.filter(role="supplier"),
        widget=forms.Select(attrs={"class": "form-select select2"}),
    )

    client = forms.ModelChoiceField(
        queryset=Party.objects.filter(role="client"),
        widget=forms.Select(attrs={"class": "form-select select2"}),
    )

    carrier = forms.ModelChoiceField(
        queryset=Party.objects.filter(role="carrier"),
        widget=forms.Select(attrs={"class": "form-select select2"})
    )

    next_destiny = forms.ModelChoiceField(
        queryset=Party.objects.filter(role="client"),
        widget=forms.Select(attrs={"class": "form-select select2"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 Exibição: "ID - Nome"
        self.fields["supplier"].label_from_instance = (
            lambda obj: f"{obj.id} - {obj.entity.name}"
        )
        self.fields["client"].label_from_instance = (
            lambda obj: f"{obj.id} - {obj.entity.name}"
        )
        self.fields["carrier"].label_from_instance = (
            lambda obj: f"{obj.id} - {obj.entity.name}"
        )
        self.fields["next_destiny"].label_from_instance = (
            lambda obj: f"{obj.id} - {obj.entity.name}"
        )

    def clean(self):
        cleaned = super().clean()

        mode = cleaned.get("creation_mode")
        cte_files = cleaned.get("cte_files", [])
        nfe_files = cleaned.get("nfe_files", [])

        if mode == "cte" and not cte_files:
            raise forms.ValidationError(
                "No modo CT-e é obrigatório anexar pelo menos um arquivo."
            )

        if mode == "nfe" and not nfe_files:
            raise forms.ValidationError(
                "No modo NF-e é obrigatório anexar pelo menos um arquivo."
            )

        return cleaned
