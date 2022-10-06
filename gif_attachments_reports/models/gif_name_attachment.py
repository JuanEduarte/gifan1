from odoo import api, fields, models


class NameAttachment(models.Model):
    _name = 'name.attachment'

    name = fields.Char(string="Nombre Adjunto")