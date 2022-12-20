
from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    # == PAC web-services ==
    l10n_mx_edi_pac = fields.Selection(
        selection=[('finkok', 'Quadrum (formerly finkok)'),
                    ('solfact', 'Solucion Factible'),
                    ('sw', 'SW sapien-SmarterWEB'),
                    ('ekomercio','Ekomercio')],
        string='PAC',
        help='The PAC that will sign/cancel the invoices',
        default='finkok')

    # l10n_mx_edi_pac = fields.Selection(selection_add=[('ekomercio','Ekomercio')])
