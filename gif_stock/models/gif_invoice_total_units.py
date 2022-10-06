from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'account.move.line'

    related_type = fields.Many2one(comodel_name='stock.picking')
    gif_total_units= fields.Float(string=' Unidades totales', compute='unidades_totales') 
    unit_type= fields.Many2one(comodel_name='uom.uom')

    def unidades_totales(self): 
        for record in self:
            unit = record.unit_type.name
            if unit == 'Tarima':
                res= record.product_uom_qty * 50
                record.gif_total_units=res
            elif unit == 'Empaque':
                res= record.product_uom_qty * 20
                record.gif_total_units=res
            elif unit == 'Docenas':
                res= record.product_uom_qty * 12
                record.gif_total_units=res
            elif unit == 'Unidades':
                res= record.product_uom_qty * 1
                record.gif_total_units=res
            else:
                record.gif_total_units=0
                