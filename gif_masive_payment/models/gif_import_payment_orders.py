from odoo import api, fields, models


class GifmasivePayment(models.Model):
    _name ='gif.masive.payment'
    _description = 'Carga de pagos masivos'

    name = fields.Char(string='Name')
    gif_payments = {}

    def masive_payment(self):
     for record in self:
         pass
         