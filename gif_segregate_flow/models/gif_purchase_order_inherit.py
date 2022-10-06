from odoo import models,api,fields


class PurchaseOrderSegregateFlow(models.Model):
    _inherit = 'purchase.order'

    amount_tax_show = fields.Monetary(string='Impuestos', compute='_amount_all_show')
    amount_untaxed_show = fields.Monetary(string='Importe sin impuestos', compute='_amount_all_show')
    amount_total_show = fields.Monetary(string='Total', compute='_amount_all_show')

    @api.depends('order_line.price_total')
    def _amount_all_show(self):
        for order in self:
            amount_untaxed_show = amount_tax_show = 0.0
            if order.sum_purchase_order == 31:
                for line in order.order_line:
                    line._compute_amount()
                    amount_untaxed_show += line.price_subtotal
                    amount_tax_show += line.price_tax
            elif order.sum_purchase_order == 1:
                for line in order.order_line:
                    if order.is_primary_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 2:
                for line in order.order_line:
                    if order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 4:
                for line in order.order_line:
                    if order.is_office_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 8:
                for line in order.order_line:
                    if order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 16:
                for line in order.order_line:
                    if order.is_ben_dis_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 3:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 9:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 17:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_ben_dis_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 5:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_office_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 10:
                for line in order.order_line:
                    if order.is_insume_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 24:
                for line in order.order_line:
                    if order.is_ben_dis_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 12:
                for line in order.order_line:
                    if order.is_office_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 18:
                for line in order.order_line:
                    if order.is_insume_purchase or order.is_ben_dis_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 6:
                for line in order.order_line:
                    if order.is_office_purchase or order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 20:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_office_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 11:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_insume_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 25:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_ben_dis_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 13:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_office_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 19:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_office_purchase or order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 7:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_office_purchase or order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 21:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_ben_dis_purchase or order.is_office_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 26:
                for line in order.order_line:
                    if order.is_insume_purchase or order.is_ben_dis_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 14:
                for line in order.order_line:
                    if order.is_insume_purchase or order.is_office_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 22:
                for line in order.order_line:
                    if order.is_ben_dis_purchase or order.is_office_purchase or order.is_insume_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 15:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_insume_purchase or order.is_office_purchase or order.is_associated_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 23:
                for line in order.order_line:
                    if order.is_primary_purchase or order.is_insume_purchase or order.is_office_purchase or order.is_ben_dis_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 27:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_insume_purchase or order.is_ben_dis_purchase or order.is_primary_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 28:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_office_purchase or order.is_ben_dis_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 29:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_office_purchase or order.is_ben_dis_purchase or order.is_primary_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 30:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_insume_purchase or order.is_ben_dis_purchase or order.is_office_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_purchase_order == 31:
                for line in order.order_line:
                    if order.is_associated_purchase or order.is_insume_purchase or order.is_ben_dis_purchase or order.is_office_purchase or order.is_primary_purchase:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id
            order.update({
                'amount_untaxed_show': currency.round(amount_untaxed_show),
                'amount_tax_show': currency.round(amount_tax_show),
                'amount_total_show': amount_untaxed_show + amount_tax_show,
            })
