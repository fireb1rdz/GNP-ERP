from django.forms import ModelForm
from django import forms
from apps.entities.models import Entity
from domain.bootstrap.service_container import get_party_service

class EntityForm(ModelForm):
    client = forms.BooleanField(required=False)
    carrier = forms.BooleanField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        party_service = get_party_service()
        existing_roles = party_service.get_existing_roles()
        selected_roles = []

        for role, translation in existing_roles:
            if cleaned_data.get(role):
                selected_roles.append((role, translation))

        if not selected_roles:
            raise forms.ValidationError("A entidade deve ter pelo menos um papel.")

        for role, translation in selected_roles:
            if not party_service.can_be(self.instance, role):
                raise forms.ValidationError(f"A entidade não pode ser um {translation}.")
        
        return cleaned_data

    class Meta:
        model = Entity
        fields = [
            "name", "cpf", "cnpj", "cpforcnpj",
            "is_active", "client",
            "carrier", "is_branch",
            "is_system", "economic_group"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control"}),
            "cpforcnpj": forms.Select(attrs={"class": "form-select"}),

            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "client": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "carrier": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_branch": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_system": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "economic_group": forms.Select(attrs={"class": "form-select"}),
        }
        