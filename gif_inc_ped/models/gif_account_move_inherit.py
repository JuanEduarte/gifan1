from odoo import models,api,fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    gif_has_pediment = fields.Char(string='Pedimento Asociado')
    gif_no_show_pediment = fields.Boolean(compute='_compute_landed_costs_visible_gif')

    def _compute_landed_costs_visible_gif(self):
        self.gif_no_show_pediment = False
        if self.gif_has_pediment != False:
            self.gif_no_show_pediment = True
        else:
            for cost in self.invoice_line_ids:
                if cost.is_landed_costs_line == True:
                    self.gif_no_show_pediment = True
                    break