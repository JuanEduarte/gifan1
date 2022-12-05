import base64
import os
import csv
import tempfile
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date


class gif_masive_payment_form(models.Model):

    _name = 'gif.masive.payment'

    name = fields.Char(string='Borrador de pago masivo')
    file_data = fields.Binary('Archivo', required=True,)
    file_name = fields.Char('nombre del archivo')
    gif_journal = fields.Many2one(comodel_name='account.journal', string='Diario', domain="[('type', '=', 'bank')]")
    confirm = fields.Char(string='Confirmar')
    client = fields.Char(string='Cliente')
    invoice_id = fields.Char(string='Factura')
    amount = fields.Char(string='Monto')
    total = fields.Char(string='Total')
    date_up = fields.Date(string='Fecha de carga')
    date_vd = fields.Date(string='Fecha de validacion')
    Memo = fields.Char(string='Memo')
    Payment_type = fields.Many2one(comodel_name='l10n_mx_edi.payment.method', string='Forma de pago')
    account = fields.Char(string='Cuenta bancaria de la empresa')
    client = fields.Many2one(comodel_name='res.partner',string='Cliente')
            


    gif_masive_payment_wzr = fields.One2many(
        comodel_name='gif.masive.payment.line', inverse_name='gif_masive_payment', string='ax', store = True)
    memo = []

    def files_data(self):
        file_path = tempfile.gettempdir()+'/file.csv'
        data = self.file_data
        f = open(file_path, 'wb')
        f.write(base64.b64decode(data))
        f.close()
        archive = csv.DictReader(open(file_path))
        
        
        client_list = []
        archive_lines = []
        total = 0
        
        
        for line in archive:
            total += float(line['Importe'])
            self.memo.append(str(line['Factura de venta']))
            if line['Cliente'] != '':
                client_list.append(line['Cliente'])
            unique = list(set(client_list))
            l = len(unique)
            if l != 1:
                raise UserError(("Las facturas cargadas no pertenecen al mismo cliente!"))
            else:
                clt = client_list[0]
                archive_lines.append(line)
                invoice = line['Factura de venta']
                inv = self.env['account.move'].search([('name', '=', invoice)])
                rel = self.env['gif.masive.payment.line'].create([{
                            'gif_masive_payment': self.id,
                            'client': clt,
                            'invoice_id': line['Factura de venta'],
                            'amount':line['Importe'],
                        }])
                partner_id = self.env['res.partner'].search([('name', '=', clt)])
            
        self.total = total
        self.Memo = self.memo
        self.client = partner_id[0]
        
    @api.onchange('gif_journal')
    def gif_journal_onchange(self):
        for record in self:
            record.account = record.client.bank_account_count
    
    def return_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.register',
            'view_type': 'form',
            'view_mode': 'form',
            }

class GifMasivePaymentLine(models.Model):
    _name = 'gif.masive.payment.line'
    _inherit = 'gif.masive.payment'
    _description = 'Linea de pago masivo'

    client = fields.Char(string='Cliente')
    invoice_id = fields.Char(string='Factura')
    amount = fields.Char(string='Importe')
    partner = fields.Char(string='Partner')

    gif_masive_payment = fields.Many2one(
        comodel_name='gif.masive.payment')

 