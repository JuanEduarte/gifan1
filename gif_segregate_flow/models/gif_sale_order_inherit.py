from odoo import api,fields,models

class SaleOrderSegregateFlow(models.Model):
    _inherit = 'sale.order'

    amount_tax_show = fields.Monetary(string='Impuestos', compute='_amount_all_show')
    amount_untaxed_show = fields.Monetary(string='Importe sin impuestos', compute='_amount_all_show')
    amount_total_show = fields.Monetary(string='Total', compute='_amount_all_show')

    @api.depends('order_line.price_total')
    def _amount_all_show(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed_show = amount_tax_show = 0.0
            if order.sum_sale_order == 7:
                for line in order.order_line:
                    if order.is_primary_sale or order.is_office_sale or order.is_ben_dis_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_sale_order == 1:
                for line in order.order_line:
                    if order.is_primary_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                        break
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_sale_order == 2:
                for line in order.order_line:
                    if order.is_office_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_sale_order == 4:
                for line in order.order_line:
                    if order.is_ben_dis_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0     
            elif order.sum_sale_order == 3:
                for line in order.order_line:
                    if order.is_primary_sale or order.is_office_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0
            elif order.sum_sale_order == 5:
                for line in order.order_line:
                    if order.is_primary_sale or order.is_ben_dis_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0 
            elif order.sum_sale_order == 6:
                for line in order.order_line:
                    if order.is_office_sale or order.is_ben_dis_sale:
                        amount_untaxed_show += line.price_subtotal
                        amount_tax_show += line.price_tax
                    else:
                        amount_untaxed_show = 0
                        amount_tax_show = 0       
            order.update({
                'amount_untaxed_show': amount_untaxed_show,
                'amount_tax_show': amount_tax_show,
                'amount_total_show': amount_untaxed_show + amount_tax_show,
            })
