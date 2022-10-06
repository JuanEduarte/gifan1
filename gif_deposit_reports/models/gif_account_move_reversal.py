from odoo import models, fields


class GifAccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    gif_concept = fields.Selection([('1','Devolución'),
                                    ('2','Descuento'),
                                    ('3','Cancelación')],
                                    string="Concepto:",
                                    default='1')
