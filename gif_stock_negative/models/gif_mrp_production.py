from odoo.exceptions import UserError
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit="mrp.production"


    def button_mark_done(self):
        for record in self:
            res = super(MrpProduction,self).button_mark_done()
            print(record.components_availability)
            if record.components_availability == 'No disponible':
                raise UserError(("No tiene Material Necesario para la Orden de Fabricación"))
            return res

    ####################################################################

    def _compute_components(self):
        for record in self:
            opera = False
            for move in record.move_raw_ids:
                if type(move.id) == int:
                    opera = True
                if record.state == 'progress' and opera == True :
                    if record.components_availability == 'No disponible':
                        raise UserError(("No tiene Material Necesario para la Orden de Fabricación"))

    ################################################################
    @api.depends(
        'move_raw_ids.state', 'move_raw_ids.quantity_done', 'move_finished_ids.state',
        'workorder_ids.state', 'product_qty', 'qty_producing')
    def _compute_state(self):            
        for record in self:
            res = super(MrpProduction,self)._compute_state()
            record._compute_components()
            print('Terminado')
            return res

# class StockMove(models.Model):
#     _inherit = 'stock.move'
#     gif_checker_employer=fields.Boolean(string="Empleados", default=False)