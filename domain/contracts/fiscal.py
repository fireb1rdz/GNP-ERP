from abc import ABC, abstractmethod

class FiscalServiceInterface(ABC):
    @abstractmethod
    def import_document(self, xml):
        """
        Importa um XML de documento fiscal e retorna um objeto com os dados.
        """
        pass
