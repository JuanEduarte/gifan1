from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    Clave_STCC = fields.Char(string='Clave STCC')
    
    
    def prductproduct(self):
        self.env['product.product'].create([{
            'product_variant_ids': self.id,
            'Clave_STCC': self.Clave_STCC
    }])  


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    NRegTributario = fields.Char(string='Numero de registro tributario')


class Vehicle(models.Model):
    _inherit = 'l10n_mx_edi.vehicle'
    
    cargo_insurer = fields.Char(string='Aseguradora de carga')
    cargo_policy  = fields.Char(string='Poliza de carga')
    sure_prime    = fields.Char(string='Prima de seguro')



class ProductProduct(models.Model):
    _inherit = 'product.product'
    ClaveSTCC = fields.Char(string='Clave STCC')

    