from abc import ABC, abstractmethod

class AccountServiceInterface(ABC):
    @abstractmethod
    def create_account(self, tenant, data):
        pass

    @abstractmethod
    def update_account(self, account, data):
        pass

    @abstractmethod
    def delete_account(self, account):
        pass

    @abstractmethod
    def list_accounts(self, tenant):
        pass

    @abstractmethod
    def get_account(self, tenant, account_id):
        pass