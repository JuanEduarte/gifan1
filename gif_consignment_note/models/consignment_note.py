from odoo import api, fields, models


class ConsignmentNote(models.Model):
    _name = 'gif.consignment.note'
    _description = 'Creaciion de archivo exel con la informacion requerida de la carta porte'

    name = fields.Char(string='Name')
