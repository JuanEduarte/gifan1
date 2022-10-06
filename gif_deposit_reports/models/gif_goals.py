from odoo import api, fields, models


class GifGoals(models.Model):
    _name = 'gif.goals'
    _description = 'Metas monetarias'

    gif_customer = fields.Char(string="Cliente")
    gif_brand = fields.Char(string="Marca")
    gif_year = fields.Char(string="Año")
    gif_month = fields.Char(string="Mes")
    gif_goal = fields.Float(string="Meta monetaria")

