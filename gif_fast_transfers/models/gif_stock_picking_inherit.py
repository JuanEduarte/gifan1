from odoo import models, api, fields
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'stock.picking'

    def gif_send_transfer(self):
        origen_purchase = False
        origen_sale = False
        move = self.env['gif.fast.transfer'].search([('gif_origin','=',self.origin)])
        print('Picking: ',self.picking_type_id.name)
        print('Picking code: ',self.picking_type_id.code)
        if len(move) >= 1:
            raise ValidationError("""Ya se ha capturado está orden. Con el nombre: %s"""%(move.name))
        if self.origin == False:
            raise ValidationError('No hay nada que capturar.')
        else:
            if self.origin != False:
                origen_purchase = self.env['purchase.order'].search([('name','=',self.origin)])
                if len(origen_purchase) == 0:
                    origen_sale = self.env['sale.order'].search([('name','=',self.origin)])
                    origen_purchase = False
            if origen_purchase != False and self.picking_type_id.code == 'incoming':
                transfer = self.env['gif.fast.transfer'].create({
                    'gif_purchase_order': origen_purchase.id,
                    'gif_type': 'purchase',
                    'gif_origin': origen_purchase.name,
                    'gif_picking': self.id,
                })
                # for line in origen_purchase.order_line:
                #     capture = self.env['gif.fast.capture'].create({
                #         'gif_product': line.product_template_id.id,
                #         'gif_relation': transfer.id,
                #     })
            elif origen_sale != False and self.picking_type_id.code == 'internal':
                transfer = self.env['gif.fast.transfer'].create({
                    'gif_sale_order': origen_sale.id,
                    'gif_type': 'sale',
                    'gif_origin': origen_sale.name,
                    'gif_picking': self.id,
                })
                # for line in origen_sale.order_line:
                #     capture = self.env['gif.fast.capture'].create({
                #         'gif_product': line.product_template_id.id,
                #         'gif_relation': transfer.id,
                #     })
            else:
                return True
            action = {
            'res_id': transfer.id,
            'res_model': 'gif.fast.transfer',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('gif_fast_transfers.gif_fast_transfer_view_form').id,
            }
        return action