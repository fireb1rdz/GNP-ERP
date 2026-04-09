from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from django_tenants.utils import (
    get_tenant_model,
    get_public_schema_name,
)

def get_domain_model():
    return apps.get_model(settings.TENANT_DOMAIN_MODEL)


class Command(BaseCommand):
    help = "Garante a existência do tenant inicial e do domínio principal."

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            default="cargo.gnpsistemas.com.br",
            help="Domínio principal do tenant inicial.",
        )
        parser.add_argument(
            "--tenant-name",
            default="GNP Sistemas",
            help="Nome do tenant inicial.",
        )

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        DomainModel = get_domain_model()

        domain_name = options["domain"].strip().lower()
        tenant_name = options["tenant_name"].strip()
        public_schema = get_public_schema_name()

        self.stdout.write(
            f"Verificando tenant inicial para domínio {domain_name}..."
        )

        tenant = TenantModel.objects.filter(schema_name=public_schema).first()

        if tenant is None:
            tenant = self._create_public_tenant(
                TenantModel=TenantModel,
                schema_name=public_schema,
                tenant_name=tenant_name,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Tenant público criado com schema '{public_schema}'."
                )
            )
        else:
            changed = False

            if hasattr(tenant, "name") and not getattr(tenant, "name", None):
                tenant.name = tenant_name
                changed = True

            if changed:
                tenant.save()
                self.stdout.write(
                    self.style.SUCCESS("Tenant público atualizado.")
                )
            else:
                self.stdout.write("Tenant público já existe.")

        domain_obj = DomainModel.objects.filter(domain=domain_name).first()

        if domain_obj is None:
            DomainModel.objects.create(
                domain=domain_name,
                tenant=tenant,
                is_primary=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Domínio '{domain_name}' criado e vinculado ao schema '{tenant.schema_name}'."
                )
            )
        else:
            changed = False

            if domain_obj.tenant_id != tenant.pk:
                domain_obj.tenant = tenant
                changed = True

            if not getattr(domain_obj, "is_primary", False):
                domain_obj.is_primary = True
                changed = True

            if changed:
                domain_obj.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Domínio '{domain_name}' atualizado."
                    )
                )
            else:
                self.stdout.write(f"Domínio '{domain_name}' já existe.")

        self.stdout.write(self.style.SUCCESS("Tenant inicial garantido com sucesso."))

    def _create_public_tenant(self, TenantModel, schema_name, tenant_name):
        data = {"schema_name": schema_name}
        field_names = {field.name for field in TenantModel._meta.fields}

        if "name" in field_names:
            data["name"] = tenant_name

        if "paid_until" in field_names:
            data["paid_until"] = None

        if "on_trial" in field_names:
            data["on_trial"] = False

        tenant = TenantModel(**data)
        tenant.save()
        return tenant