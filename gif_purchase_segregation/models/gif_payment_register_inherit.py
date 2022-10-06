from odoo import models,api,fields


class AccountPaymentRegisterPS(models.TransientModel):
    _inherit = 'account.payment.register'

    type_of_purchase = fields.Many2one(comodel_name='gif.tipificaciones.compras', string='Tipo de Compra')
    gif_is_purchase = fields.Boolean(default=False,compute="_onchange_journal_id_ps_purchase")

    @api.onchange('journal_id')
    def _onchange_journal_id_ps_purchase(self):
        for record in self:
            invoice_purchase = self.env['account.move'].search([('name','=',record.communication)])
            if invoice_purchase.type_of_purchase:
                record.gif_is_purchase = True
                if invoice_purchase.type_of_purchase.id == 1:
                    record.type_of_purchase = 1
                elif invoice_purchase.type_of_purchase.id == 2:
                    record.type_of_purchase = 2
                elif invoice_purchase.type_of_purchase.id == 3:
                    record.type_of_purchase = 3
                elif invoice_purchase.type_of_purchase.id == 4:
                    record.type_of_purchase = 4
                elif invoice_purchase.type_of_purchase.id == 5:
                    record.type_of_purchase = 5
            elif invoice_purchase.type_of_sale:
                record.gif_is_purchase = False
                record.type_of_purchase = False

    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'type_of_purchase': self.type_of_purchase.id,
            'type_of_sale': self.type_of_sale.id,
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals
    
    def _create_payments(self):
        self.ensure_one()
        batches = self._get_batches()
        edit_mode = self.can_edit_wizard and (len(batches[0]['lines']) == 1 or self.group_payment)
        to_process = []

        if edit_mode:
            print('If edit mode')
            payment_vals = self._create_payment_vals_from_wizard()
            to_process.append({
                'create_vals': payment_vals,
                'to_reconcile': batches[0]['lines'],
                'batch': batches[0],
            })
            print('Estos son los to_process en el if: ',to_process)
        else:
            print('Else')
            # Don't group payments: Create one batch per move.
            if not self.group_payment:
                print('If del else')
                new_batches = []
                for batch_result in batches:
                    for line in batch_result['lines']:
                        new_batches.append({
                            **batch_result,
                            'lines': line,
                        })
                batches = new_batches

            for batch_result in batches:
                to_process.append({
                    'create_vals': self._create_payment_vals_from_batch(batch_result),
                    'to_reconcile': batch_result['lines'],
                    'batch': batch_result,
                })
                print('To process en else y for: ',to_process)

        print('Payments: ')
        payments = self._init_payments(to_process, edit_mode=edit_mode)
        self._post_payments(to_process, edit_mode=edit_mode)
        self._reconcile_payments(to_process, edit_mode=edit_mode)
        print('Estos son los payments al final: ',payments)
        print('Justo antes del final de payment')
        return payments

    def action_create_payments(self):
        print('Este es el boton')
        payments = self._create_payments()

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        print('Y devuelve: ',action)
        return action

    
