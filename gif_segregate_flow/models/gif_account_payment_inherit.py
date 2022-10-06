from odoo import models,fields,api


class AccountPaymentSegregateFlow(models.Model):
    _inherit = 'account.payment'

    amount_company_currency_signed_show = fields.Monetary(currency_field='company_currency_id', compute='_compute_amount_company_currency_signed_show')

    is_discount_sale = fields.Char(string='')
    

    @api.depends('amount_total_signed', 'payment_type')
    def _compute_amount_company_currency_signed_show(self):
        for payment in self:
            if payment.sum_payment_sale == 1 or payment.sum_payment_purchase == 1:
                if payment.is_primary_sale or payment.is_primary_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 2 or payment.sum_payment_purchase == 4:
                if payment.is_office_sale or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 3 or payment.sum_payment_purchase == 5:
                if payment.is_primary_sale or payment.is_primary_purchase or payment.is_office_sale or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 4 or payment.sum_payment_purchase == 16:
                if payment.is_ben_dis_sale or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 5 or payment.sum_payment_purchase == 17:
                if payment.is_primary_sale or payment.is_primary_purchase or payment.is_ben_dis_sale or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 6 or payment.sum_payment_purchase == 20:
                if payment.is_office_sale or payment.is_office_purchase or payment.is_ben_dis_sale or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_sale == 7:
                if payment.sum_payment_purchase == 21:
                    if payment.is_primary_sale or payment.is_primary_purchase or payment.is_office_sale or payment.is_office_purchase or payment.is_ben_dis_sale or payment.is_ben_dis_purchase:
                        if payment.payment_type == 'outbound':
                            payment.amount_company_currency_signed_show = -payment.amount_total_signed
                        else:
                            payment.amount_company_currency_signed_show = payment.amount_total_signed
                    else:
                        if payment.payment_type == 'outbound':
                            payment.amount_company_currency_signed_show = 0
                        else:
                            payment.amount_company_currency_signed_show = 0
                elif payment.sum_payment_purchase == 31:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
            elif payment.sum_payment_purchase == 8:
                if payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 2:
                if payment.is_insume_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 3:
                if payment.is_insume_purchase or payment.is_primary_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 9:
                if payment.is_associated_purchase or payment.is_primary_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 6:
                if payment.is_insume_purchase or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 7:
                if payment.is_insume_purchase or payment.is_primary_purchase or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 10:
                if payment.is_insume_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 11:
                if payment.is_insume_purchase or payment.is_primary_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 12:
                if payment.is_office_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 13:
                if payment.is_office_purchase or payment.is_primary_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 14:
                if payment.is_insume_purchase or payment.is_associated_purchase or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 15:
                if payment.is_insume_purchase or payment.is_primary_purchase or payment.is_office_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 18:
                if payment.is_insume_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 19:
                if payment.is_ben_dis_purchase or payment.is_primary_purchase or payment.is_insume_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 22:
                if payment.is_insume_purchase or payment.is_office_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 23:
                if payment.is_primary_purchase or payment.is_insume_purchase or payment.is_office_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 24:
                if payment.is_ben_dis_purchase or payment.is_associated_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 25:
                if payment.is_associated_purchase or payment.is_primary_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 26:
                if payment.is_associated_purchase or payment.is_ben_dis_purchase or payment.is_insume_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 27:
                if payment.is_primary_purchase or payment.is_associated_purchase or payment.is_ben_dis_purchase or payment.is_insume_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 28:
                if payment.is_associated_purchase or payment.is_ben_dis_purchase or payment.is_office_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 29:
                if payment.is_primary_purchase or payment.is_associated_purchase or payment.is_office_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 30:
                if payment.is_insume_purchase or payment.is_associated_purchase or payment.is_office_purchase or payment.is_ben_dis_purchase:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                    else:
                        payment.amount_company_currency_signed_show = payment.amount_total_signed
                else:
                    if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = 0
                    else:
                        payment.amount_company_currency_signed_show = 0
            elif payment.sum_payment_purchase == 31:
                if payment.payment_type == 'outbound':
                        payment.amount_company_currency_signed_show = -payment.amount_total_signed
                else:
                    payment.amount_company_currency_signed_show = payment.amount_total_signed
            else:
                payment.amount_company_currency_signed_show = 0

