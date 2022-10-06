
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gif_fill_rate= fields.Boolean(string="Fill Rete", default=False)


    def b_gif_fill_rate(self):
        pass
        

