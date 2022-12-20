
from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _l10n_mx_edi_get_cadena_xslts(self):
        return 'gif_account_edi_providers_40/data/4.0/cadenaoriginal_TFD_1_1.xslt', 'gif_account_edi_providers_40/data/4.0/cadenaoriginal_4_0.xslt'
