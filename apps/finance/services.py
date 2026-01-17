from .models import Invoice

class FinanceServiceImpl:
    def create_invoice(self, organization, amount, reference, description="Service"):
        """
        Creates an invoice.
        The caller doesn't need to know about the Invoice model.
        """
        invoice = Invoice.objects.create(
            organization=organization,
            amount=amount,
            source_reference=reference,
            description=description
        )
        return invoice
