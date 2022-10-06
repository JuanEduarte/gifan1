from odoo import models, fields


class GifAccountMove(models.Model):
    _inherit = 'account.move'

    gif_invoice_uuid = fields.Char(string="UUID", default='', size=36)


    def attachment_to_invoice_auto(self):
        print('adjuntar')
        for record in self:

            if not record.gif_invoice_uuid:
                return self.notification("Asigne un UUID a la factura.")

            # Buscamos el updater
            attached_xml = self.env['gif.purchase.xml.updater'].search([('gif_uuid','like',record.gif_invoice_uuid)])
            print("Attached:", attached_xml)

            if not attached_xml:
                return self.notification("No existe el archivo XML.")

            if attached_xml.gif_account_move:
                return self.notification("El XML ya está asociado a una factura.")

            # Buscamos los archivos adjuntos
            attached = self.env['ir.attachment'].search([('res_id', '=', attached_xml.id)])
            
            for file in attached:
                try:
                    ids = record.attachment_ids.ids
                    file.res_model = 'account.move'
                    file.res_name = record.name
                    # Asocia el XML a la factura
                    file.res_id = record.id
                    ids.append(file.id)
                    newids = [(6, 0, ids)]
                    record.update({'attachment_ids': newids})
                except:
                    # Este error no debe salir
                    print("No se pudo adjuntar el archivo:", file.name)

                else:
                    attached_xml.gif_account_move = record.id
            
            return self.notification("El XML se adjuntó correctamente.")


    def notification(self, msm):
        return {
            'name': 'Asignación automática de XML',
            'context':{'default_text_notification':msm},
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.notification',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            }





class GifAccountPayment(models.Model):
    _inherit = 'account.payment'

    gif_invoice_uuid = fields.Char(string="UUID", default='', size=36)

    