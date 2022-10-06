from odoo import models,api,fields


class AccountPaymentRegisterSA(models.TransientModel):
    _inherit = 'account.payment.register'

    type_of_sale = fields.Many2one(comodel_name='gif.tipificaciones.ventas', string='Tipo de Venta')
    gif_is_sale = fields.Boolean(default=False,compute="_onchange_journal_id_sa")

    @api.onchange('journal_id')
    def _onchange_journal_id_sa(self):
        for record in self:
            invoice_sale = self.env['account.move'].search([('name','=',record.communication)])
            if invoice_sale.type_of_sale:
                record.gif_is_sale = True
                if invoice_sale.type_of_sale.id == 1:
                    record.type_of_sale = 1
                elif invoice_sale.type_of_sale.id == 2:
                    record.type_of_sale = 2
                elif invoice_sale.type_of_sale.id == 3:
                    record.type_of_sale = 3
            elif invoice_sale.type_of_purchase:
                record.gif_is_sale = False
                record.type_of_sale = False

    
