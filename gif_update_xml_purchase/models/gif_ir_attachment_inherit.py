from odoo import models


class GifIrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('full_code'):
                xml = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.name)])
                name = f'{xml.name} / {xml.gif_uuid} / ${xml.gif_total}'
            else:
                name = record.name
            result.append((record.id,name))
        return result
