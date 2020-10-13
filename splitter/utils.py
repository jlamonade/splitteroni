from decimal import Decimal


def _check_tip_tax_then_add(self):
    # Checks to see if tip or tax is null before adding them to total else it returns 0
    total = 0
    if self.tip:
        total += Decimal(self.tip)
    if self.tax:
        total += Decimal(self.tax)
    return Decimal(total)
