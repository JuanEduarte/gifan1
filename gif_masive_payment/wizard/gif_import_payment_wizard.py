import base64
import os
import csv
import tempfile
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date


class gif_masive_payment_Wizard(models.TransientModel):

    _name = 'gif.masive.payment.wizard'

    file_data = fields.Binary('Archivo', required=True,)
    file_name = fields.Char('nombre del archivo')
    gif_journal = fields.Many2one( comodel_name='account.journal', string='Diario')
    confirm = fields.Char(string='Confirmar') 
    
    gif_masive_payment_wzr = fields.One2many(comodel_name='gif.masive.payment.line.wzr', inverse_name='gif_masive_payment', string='a')

    def files_data(self):
        file_path = tempfile.gettempdir()+'/file.csv'
        data = self.file_data
        f = open(file_path, 'wb')
        f.write(base64.b64decode(data))
        f.close()
        archive = csv.DictReader(open(file_path))

        limit = 0
        customer = []
        for l in archive:
            customer.append(l)
            p = customer[0]['Cliente']
            res = self.env['res.partner'].search([('name', '=', p)])
            if self.gif_journal:
              print('0000', self.gif_journal)

            limit += 1
            if limit > 0:
                break
            print(res.name)
            print(res.bank_ids.display_name)
            print(res.bank_ids.journal_id)
            print('****', p)

        archive_lines = []
        memo = []
        for line in archive:
            archive_lines.append(line)
            memo.append(line['Factura de venta'])
            for line in archive_lines:
                cliente = p
            print(cliente, line['Factura de venta'], line['Importe'])
            for record in self:
                if cliente:
                    rel = self.env['gif.masive.payment.line.wzr'].create([{
                        'gif_masive_payment': record.id,
                        'client': cliente,
                        'invoice_id': line['Factura de venta'],
                        'amount':line['Importe'],
                        'partner':res.bank_ids.display_name,
                    }])

                else:
                    pass
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'gif.masive.payment.wizard',
            'view_mode': 'form',
            'res_id':self.id,
            'target': 'new',
            }


class GifMasivePaymentLine(models.Model):
    _name = 'gif.masive.payment.line.wzr'
    _inherit = 'gif.masive.payment.wizard'
    _description = 'Linea de pago masivo'

    client = fields.Char(string='Cliente')
    invoice_id = fields.Char(string='Factura')
    amount = fields.Char(string='Importe')
    partner = fields.Char(string='Partner')
    memo = fields.Char(string='memo')

    gif_masive_payment = fields.Many2one(comodel_name='gif.masive.payment.wizard')
