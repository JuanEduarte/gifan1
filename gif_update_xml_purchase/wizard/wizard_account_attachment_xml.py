from odoo import fields, models, api
import base64

class WizardAccountAttachmentXML(models.TransientModel):
    _name = 'wizard.account.attachment.xml'
    _description = 'Adjuntar XML'

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
            print(record.move_id.partner_id)
            xmls = self.env['gif.purchase.xml.updater'].search([('gif_rfc_issuer', '=', record.move_id.partner_id.vat), ('gif_account_move', '=', False)])
            # xmls = self.env['gif.purchase.xml.updater'].search([])
            ids = xmls.ids
            res['domain'] = {'gif_attached_xml': [('id', '=', ids)]}
            return res

    def attachment_to_invoice(self):
        # print('adjuntar')
        for record in self:
            
            attached_files = self.env['ir.attachment'].search([('res_id', '=', record.gif_attached_xml.id)])
            for attached in attached_files:
                ids = record.move_id.attachment_ids.ids
                attached.res_model = 'account.move'
                attached.res_name = record.move_id.name
                # Asocia a la factura
                record.gif_attached_xml.gif_account_move = record.move_id.id
                attached.res_id = record.move_id.id

                ids.append(attached.id)
                new_ids = [(6, 0, ids)]
                record.move_id.update({'attachment_ids': new_ids})

            return True


class WizardAccountUnattachmentXML(models.TransientModel):
    _name = 'wizard.account.unattachment.xml'
    _description = 'Desadjuntar XML'

    move_id = fields.Many2one('account.move', string="Factura")
    move_attached = fields.Many2one('ir.attachment', string="Adjunto", context = "{'full_code':True}")

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
            print(record.move_id.name)
            ids = record.move_id.attachment_ids#.ids
            ids_lst = [att.id for att in ids if att.mimetype == 'application/xml']
            res['domain'] = {'move_attached': [('id', '=', ids_lst)]}
            return res

    def unattachment_to_invoice(self):
        # print('Desadjuntar')
        for record in self:

            xml_updater = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.move_attached.name)])

            for attached in record.move_id.attachment_ids:
                if attached.name == record.move_attached.name or attached.name == xml_updater.gif_uuid:
                    ids = record.move_id.attachment_ids.ids
                    attached.res_model = 'gif.purchase.xml.updater'
                    attached.res_name = ''
                    xml_updater.gif_account_move = False
                    attached.res_id = xml_updater.id

                    ids.remove(attached.id)
                    record.move_id.update({'attachment_ids': [(6, 0, ids)] })
            
            return True

class WizardPaymentAttachmentXML(models.TransientModel):
    _name = 'wizard.payment.attachment.xml'
    _description = 'Adjuntar XML'

    payment_id = fields.Many2one('account.payment', string="Pago")
    gif_attached_xml = fields.Many2one('gif.purchase.xml.updater', string="Adjunto")

    @api.model
    def default_get(self, fields):
        rec = super(WizardPaymentAttachmentXML, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['payment_id'] = id_ctx
        return rec

    # @api.onchange('payment_id')
    # def get_purchase(self):
    #     for record in self:
    #         res = {}
    #         print(record.payment_id.partner_id)
    #         xmls = self.env['gif.purchase.xml.updater'].search([('gif_rfc_issuer', '=', record.payment_id.partner_id.vat), ('gif_account_payment', '=', False)])
    #         # xmls = self.env['gif.purchase.xml.updater'].search([])
    #         ids = xmls.ids
    #         res['domain'] = {'gif_attached_xml': [('id', '=', ids)]}
    #         return res

    def attachment_to_payment(self):
        print('adjuntar')
        for record in self:
            attached_files = self.env['ir.attachment'].search([('res_id', '=', record.gif_attached_xml.id)])
            for attached in attached_files:
                ids = record.payment_id.attachment_ids.ids
                attached.res_model = 'account.payment'
                attached.res_name = record.payment_id.name
                # Asocia a la factura
                record.gif_attached_xml.gif_account_payment = record.payment_id.id
                attached.res_id = record.payment_id.id

                ids.append(attached.id)
                new_ids = [(6, 0, ids)]
                record.payment_id.update({'attachment_ids': new_ids})

            return True

        # for record in self:
        #     attached = self.env["ir.attachment"].search([('name', '=', record.gif_attached_xml.gif_filename)])
        #     ids = record.payment_id.attachment_ids.ids
        #     attached.res_model = 'account.payment'
        #     attached.res_name = record.payment_id.name
        #     record.gif_attached_xml.gif_account_payment = record.payment_id.id
        #     attached.res_id = record.payment_id.id
        #     print(ids)
        #     print(attached.name)
        #     ids.append(attached.id)
        #     print(ids)
        #     print(attached.name)

        #     return True

class WizardPaymentUnattachmentXML(models.TransientModel):
    _name = 'wizard.payment.unattachment.xml'
    _description = 'Desadjuntar XML'

    payment_id = fields.Many2one('account.payment', string="Pago")
    move_attached = fields.Many2one('ir.attachment', string="Adjunto")

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
            ids = record.payment_id.attachment_ids#.ids
            ids_lst = [att.id for att in ids if att.mimetype == 'application/xml']
            res['domain'] = {'move_attached': [('id', '=', ids_lst)]}
        
            #res = {}
            #attach = self.env['ir.attachment'].search([('res_id', '=', record.payment_id.id)])
            #res['domain'] = {'move_attached': [('id', '=', attach.ids)]}
            return res

    def unattachment_to_payment(self):
        print('Desadjuntar')
        for record in self:
            xml_updater = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.move_attached.name)])

            for attached in record.payment_id.attachment_ids:
                if attached.name == record.move_attached.name or attached.name == xml_updater.gif_uuid:
                    ids = record.payment_id.attachment_ids.ids
                    attached.res_model = 'gif.purchase.xml.updater'
                    attached.res_name = ''
                    xml_updater.gif_account_move = False
                    attached.res_id = xml_updater.id

                    ids.remove(attached.id)
                    record.payment_id.update({'attachment_ids': [(6, 0, ids)] })

            # attached = self.env["ir.attachment"].search([('name', '=', record.move_attached.name)])
            # xml_updater = self.env['gif.purchase.xml.updater'].search([('gif_filename', '=', record.move_attached.name)])
            # ids = record.payment_id.attachment_ids.ids
            # attached.res_model = 'gif.purchase.xml.updater'
            # attached.res_name = ''
            # xml_updater.gif_account_payment = False
            # attached.res_id = xml_updater.id

            # ids.remove(attached.id)
            # attached = [(6, 0, ids)]
            # record.payment_id.update({'attachment_ids': attached})

            return True