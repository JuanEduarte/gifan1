from odoo import api, fields, models

class SalesReport(models.Model):
    _name = 'sales.report'
    _description = 'Reportes de ventas'

    name = fields.Char(string='Name')
    company = fields.Many2one(comodel_name='res.company', string='Empresa')
    Date = fields.Date(string='Fecha')
    
    
