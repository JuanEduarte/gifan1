from platform import release
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class GifStockMove(models.Model):
    _inherit="stock.move"
    

    @api.onchange('move_line_nosuggest_ids')
    def _counter_qty_lines(self):
        for record in self:
            counter = 0
            for line in record.move_line_nosuggest_ids:
                counter += line.qty_done
            print(counter)
            if counter > record.product_uom_qty:
                raise UserError(_("Tu cantidad hecha es mayor a tu cantidad demandada."))






