from email.policy import default
from odoo import models, fields, api

class GifPalletPallet(models.Model):
    _name = 'gif.pallet.pallet'
    _description = 'Modelo de Tarimas'

    name = fields.Char(string='Nombre', default='Control de Tarimas')
    gif_counter_standard = fields.Integer(string='Tarima Estandar')
    gif_counter_chep = fields.Integer(string='Tarima Chep')
    gif_counter_smart = fields.Integer(string='Tarima Smart')
    gif_counter_other = fields.Integer(string='Tarima Otras')
    gif_history_pallet = fields.One2many('gif.history.pallet', 'gif_pallet_id', string='Historico de Tarimas')
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company.id)

class GifHistoricPallet(models.Model):
    _name = 'gif.history.pallet'
    _description = 'Modelo de Historial de Tarimas'

    name = fields.Char(string='Nombre')
    stock_picking = fields.Char(string='Referencia')
    partner_id = fields.Many2one('res.partner', string='Clientes')
    gif_date_historic = fields.Datetime(string='Fecha')
    gif_standard_before = fields.Integer(string='Estandar antes')
    gif_standard_after = fields.Integer(string='Estandar despues')
    gif_chep_before = fields.Integer(string='Chep antes')
    gif_chep_after = fields.Integer(string='Chep despues')
    gif_smart_before = fields.Integer(string='Smart antes')
    gif_smart_after = fields.Integer(string='Smart despues')
    gif_other_before = fields.Integer(string='Otras antes')
    gif_other_after = fields.Integer(string='Otras despues')
    gif_pallet_id = fields.Many2one('gif.pallet.pallet', string="Tarima")