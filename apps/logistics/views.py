from apps.entities.models import Party
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView
from .models import Conference
# from domain.schemas.conference_table import ConferenceTableSchema
from domain.bootstrap.service_container import get_conference_application_service
from .forms import ConferenceCreateForm
from domain.registry.module_registry import ModuleRegistry

class ConferenceCreateView(View):
    template_name = "logistics/conference_create.html"

    def get(self, request):
        form = ConferenceCreateForm()
        logged_entity = request.user.entity
        if Party.objects.filter(entity=logged_entity, role="carrier").exists():
            form.fields["destination"].initial = Party.objects.get(entity=logged_entity, role="carrier")
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        logged_entity = request.user.entity

        form = ConferenceCreateForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        creation_mode = form.cleaned_data["creation_mode"]
        cte_files = form.cleaned_data["cte_files"]
        nfe_files = form.cleaned_data["nfe_files"]
        supplier = form.cleaned_data["supplier"]
        client = form.cleaned_data["client"]
        next_destiny = form.cleaned_data["next_destiny"]
        access_keys = form.cleaned_data["access_keys"]
        access_keys = access_keys.replace('"', '')
        access_keys = access_keys.replace('[', '')
        access_keys = access_keys.replace(']', '')
        access_keys = access_keys.split(',')

        try:
            with transaction.atomic():
                if creation_mode == "access_key":
                    for key in access_keys:
                        print(key)
            messages.success(request, "Conferência criada com sucesso.")
            return redirect("logistics:conference_list")

        except Exception as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {"form": form})

class ConferenceListView(ListView):
    model = Conference
    context_object_name = "conferences"
    paginate_by = 10

    def get_queryset(self):
        return Conference.objects.filter(tenant=self.request.tenant)

