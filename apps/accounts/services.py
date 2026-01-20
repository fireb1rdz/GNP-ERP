from apps.core.services.accounts import AccountServiceInterface
from apps.accounts.models import User
from django.core.exceptions import ValidationError

class AccountService(AccountServiceInterface):
    def create_account(self, tenant, data):
        required_fields = ['username', 'password', 'email']

        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            raise ValidationError(
                f'Campos obrigatórios ausentes: {", ".join(missing)}'
            )

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],  # hash automático
            email=data.get('email'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            tenant=tenant
        )

        return user

    def update_account(self, account, data):
        account.username = data.get('username', account.username)
        account.email = data.get('email', account.email)
        account.first_name = data.get('first_name', account.first_name)
        account.last_name = data.get('last_name', account.last_name)

        if 'password' in data:
            account.set_password(data['password'])

        account.save()
        return account

    def delete_account(self, account):
        account.delete()
        return True

    def list_accounts(self, tenant):
        return User.objects.filter(tenant=tenant)

    def get_account(self, tenant, account_id):
        return User.objects.get(tenant=tenant, id=account_id)
