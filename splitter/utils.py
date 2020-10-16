from decimal import Decimal


def _check_tip_tax_then_add(self):
    # Checks to see if tip or tax is null before adding them to total else it returns 0
    total = 0
    tip = self.get_tip_amount()
    tax = self.get_tax_amount()
    if tip:
        total += tip
    if tax:
        total += tax
    return Decimal(total)
