

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    def _prepare_edi_vals_to_export(self):
        for tag in self.tax_ids:
            tax_iva = tag.amount if 'IVA' in tag.name else 0.0
            tax_ieps = tag.amount if 'IEPS' in tag.name else 0.0

        vals = {
            **super(self)._prepare_edi_vals_to_export(),
            'tax_iva':tax_iva,
            'tax_ieps':tax_ieps,
        }

        return  vals
                