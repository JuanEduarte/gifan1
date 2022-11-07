from odoo.exceptions import UserError, ValidationError
from odoo import models, fields


class GifAccountMove(models.Model):
    _inherit = 'account.move'

    gif_invoice_uuid = fields.Char(string="UUID", default='', size=36)


    def attachment_updater(self, updater=None):
        for record in self:

            # Se adjunta automaticamente
            if not updater:
                
                if not record.gif_invoice_uuid:
                    raise UserError("Asigne un UUID a la factura.")

                # Buscamos el updater
                updater = self.env['gif.purchase.xml.updater'].search([('gif_uuid','like',record.gif_invoice_uuid)])

                if not updater:
                    raise ValidationError("Ningún archivo XML contiene el UUID de la factura.")

            if updater.gif_account_move:
                raise ValidationError("El archivo XML ya está asociado a una factura.")

            if updater.gif_account_payment:
                raise ValidationError("El archivo XML ya está asociado a un pago.")

            # Buscamos los archivos adjuntos
            attached = self.env['ir.attachment'].search([('res_id', '=', updater.id)])
            
            for file in attached:
                try:
                    # Actualizamos datos
                    file.res_model = 'account.move'
                    file.res_name = record.name
                    # Asocia el XML a la factura
                    file.res_id = record.id
                    updater.gif_account_move = record.id
                    
                    record.update({'attachment_ids': [(4,file.id)]})

                except:
                    # Este error no debe salir
                    raise ValidationError("No se pudo adjuntar el archivo: " + file.name)
                
            else:
                self.notification("El archivo XML se ha adjuntado correctamente.")


    def attachment_file(self, updater, file):
        for record in self:

            try:
                file.res_model = 'account.move'
                file.res_name = record.name
                # Asocia el XML al pago
                file.res_id = record.id
                updater.gif_account_move = record.id
                record.update({'attachment_ids': [(4,updater.id)]})
            except:
                # Este error no debe salir
                raise ValidationError("No se pudo adjuntar el archivo:", file.name)


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

    gif_payment_uuid = fields.Char(string="UUID", default='', size=36)
    
    def attachment_updater(self, updater=None):
        for record in self:

            # Se adjunta automaticamente
            if not updater:
                
                if not record.gif_payment_uuid:
                    raise UserError("Asigne un UUID al pago.")
                
                # Buscamos el updater
                updater = self.env['gif.purchase.xml.updater'].search([('gif_uuid','like',record.gif_payment_uuid)])

                # Validaciones
                if not updater:
                    raise ValidationError("No existe el archivo XML.")

            if updater.gif_account_move:
                raise ValidationError("El archivo XML ya está asociado a una factura.")

            if updater.gif_account_payment:
                raise ValidationError("El archivo XML ya está asociado a un pago.")

            # Buscamos los archivos adjuntos
            attached = self.env['ir.attachment'].search([('res_id', '=', updater.id)])

            for file in attached:
                try:
                    file.res_model = 'account.payment'
                    file.res_name = record.name
                    # Asocia el XML al pago
                    file.res_id = record.id
                    updater.gif_account_payment = record.id
                    record.update({'attachment_ids': [(4,updater.id)]})
                except:
                    # Este error no debe salir
                    raise ValidationError("No se pudo adjuntar el archivo:", file.name)
    
    def attachment_file(self, updater, file):
        for record in self:

            try:
                file.res_model = 'account.payment'
                file.res_name = record.name
                # Asocia el XML al pago
                file.res_id = record.id
                updater.gif_account_payment = record.id
                record.update({'attachment_ids': [(4,updater.id)]})
            except:
                # Este error no debe salir
                raise ValidationError("No se pudo adjuntar el archivo:", file.name)