from odoo import fields, models, api
import base64
from odoo.exceptions import UserError, ValidationError

class WizardAccountAttachmentXML(models.TransientModel):
    _name = 'wizard.account.attachment.xml'
    _description = 'Adjuntar XML a Facturas'

    move_id = fields.Many2one('account.move', string="Factura")
    gif_attached_xml = fields.Many2one('gif.purchase.xml.updater', string="Adjunto", context = "{'full_code':True}")

    @api.model
    def default_get(self, fields):
        rec = super(WizardAccountAttachmentXML, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['move_id'] = id_ctx
        return rec
    
    @api.onchange('move_id')
    def get_purchase(self):
        for record in self:
            res = {}
            # print(record.move_id.partner_id)
            xmls = self.env['gif.purchase.xml.updater'].search([('gif_rfc_issuer', '=', record.move_id.partner_id.vat), ('gif_account_move', '=', False)])
            # xmls = self.env['gif.purchase.xml.updater'].search([])
            ids = xmls.ids
            res['domain'] = {'gif_attached_xml': [('id', '=', ids)]}
            return res

    def attachment_to_invoice(self):
        for record in self:
            record.move_id.attachment_updater(record.gif_attached_xml)
            return True



class WizardAccountUnattachmentXML(models.TransientModel):
    _name = 'wizard.account.unattachment.xml'
    _description = 'Desadjuntar XML de Facturas'

    move_id = fields.Many2one('account.move', string="Factura")
    move_attached = fields.Many2one('ir.attachment', string="Adjunto")#, context = "{'full_code':True}")

    @api.model
    def default_get(self, fields):
        rec = super(WizardAccountUnattachmentXML, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['move_id'] = id_ctx
        return rec

    @api.onchange('move_id')
    def get_purchase(self):
        for record in self:
            res = {}
            attach = self.env['ir.attachment'].search([('res_id', '=', record.move_id.id),('mimetype','=','application/xml')])
            res['domain'] = {'move_attached': [('id', '=', attach.ids)]}
            return res

    def unattachment_to_invoice(self):
        print('Desadjuntar move')
        for record in self:
            xml_updater = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.move_attached.name)])
            # print(xml_updater, xml_updater.name, xml_updater.gif_account_move)

            attachment_ids = self.env['ir.attachment'].search([('res_id', '=', record.move_id.id)])
            # print("Att_ids:", attachment_ids)

            for attached in attachment_ids:
                if attached.name in (record.move_attached.name, xml_updater.gif_uuid):
                    # print(attached.name)
                    ids = self.move_id.attachment_ids.ids
                    attached.res_model = 'gif.purchase.xml.updater'
                    attached.res_name = xml_updater.name
                    
                    attached.res_id = xml_updater.id
                    xml_updater.gif_account_move = False

                    ids.remove(attached.id)
                    new_ids = [(6, 0, ids)]
                    record.move_id.update({'attachment_ids': new_ids })


            print(self.env['ir.attachment'].search([('res_id', '=', xml_updater.id)]))

            return True



class WizardPaymentAttachmentXML(models.TransientModel):
    _name = 'wizard.payment.attachment.xml'
    _description = 'Adjuntar XML a Pagos'

    payment_id = fields.Many2one('account.payment', string="Pago")
    gif_attached_xml = fields.Many2one('gif.purchase.xml.updater', string="Adjunto", context = "{'full_code':True}")

    @api.model
    def default_get(self, fields):
        rec = super(WizardPaymentAttachmentXML, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['payment_id'] = id_ctx
        return rec
        

    @api.onchange('payment_id')
    def get_purchase(self):
        for record in self:
            res = {}
            # print(record.payment_id.partner_id)
            xmls = self.env['gif.purchase.xml.updater'].search([('gif_rfc_issuer', '=', record.payment_id.partner_id.vat), ('gif_account_payment', '=', False)])
            # xmls = self.env['gif.purchase.xml.updater'].search([])
            ids = xmls.ids
            res['domain'] = {'gif_attached_xml': [('id', '=', ids)]}
            return res

    def attachment_to_payment(self):
        for record in self:
            record.payment_id.attachment_updater(record.gif_attached_xml)
            return True



class WizardPaymentUnattachmentXML(models.TransientModel):
    _name = 'wizard.payment.unattachment.xml'
    _description = 'Desadjuntar XML de Pagos'

    payment_id = fields.Many2one('account.payment', string="Pago")
    move_attached = fields.Many2one('ir.attachment', string="Adjunto",context = "{'full_code':True}")

    @api.model
    def default_get(self, fields):
        rec = super(WizardPaymentUnattachmentXML, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['payment_id'] = id_ctx
        return rec

    @api.onchange('payment_id')
    def get_purchase(self):
        for record in self:
            res = {}
            attach = self.env['ir.attachment'].search([('res_id', '=', record.payment_id.id),('mimetype','=','application/xml')])
            res['domain'] = {'move_attached': [('id', '=', attach.ids)]}
            return res

    def unattachment_to_payment(self):
        """Función que desadjunta el XML y PDF de un pago.
            FUNCIONAL
        """
        # print('Desadjuntar :u')
        for record in self:
            xml_updater = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.move_attached.name)])

            attachment_ids = self.env['ir.attachment'].search([('res_id', '=', record.payment_id.id)])
            
            for attached in attachment_ids:
                if attached.name == record.move_attached.name or attached.name == xml_updater.gif_uuid:
                    # ids = self.move_id.attachment_ids.ids
                    # print(attached.name)
                    attached.res_model = 'gif.purchase.xml.updater'
                    attached.res_name = xml_updater.name
                    
                    attached.res_id = xml_updater.id
                    xml_updater.gif_account_payment = False

                    # ids.remove(attached.id)
                    # new_ids = [(6, 0, ids)]
                    # record.move_id.update({'attachment_ids': new_ids })
                    record.payment_id.update({'attachment_ids': [(3, attached.id)] })

            return True