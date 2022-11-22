from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NamaModel(models.Model):
    _inherit = 'product.template'

    Clave_STCC = fields.Char(string='Clave STCC')  


class NamaModel(models.Model):
    _inherit = 'res.partner'
    
    NRegTributario = fields.Char(string='Numero de registro tributario')


class NamaModel(models.Model):
    _inherit = 'l10n_mx_edi.vehicle'
    
    cargo_insurer = fields.Char(string='Aseguradora de carga')
    cargo_policy  = fields.Char(string='Poliza de carga')
    sure_prime    = fields.Char(string='Prima de seguro')