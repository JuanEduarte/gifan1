from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    related_type = fields.Many2one(comodel_name='stock.picking')
    gif_total_units= fields.Float(string=' Unidades totales', compute='total_units') 
    unit_type= fields.Many2one(comodel_name='uom.uom')

    def total_units(self):
        for record in self:
          record.gif_total_units = record.product_uom.ratio
                