from odoo import api, fields, models
import json
from odoo.tools.misc import formatLang

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"
    
    gif_IepsDisplayOL = fields.Boolean(compute='_get_display_ol')
    gif_SaleOrderIeps = fields.Float(string='IEPS',store=True) #compute='_onchange_price_unit_gif_ieps'
    gif_SaleOrderIepsChar = fields.Char(string='IEPS Char',readonly=True,store=True)
    gif_price_unit_ieps = fields.Float(string='GIF Precio Unitario',compute='_gif_onchange_price_unit_ieps')
    gif_price_subtotal_ieps = fields.Float(string='GIF Subtotal',compute='_gif_onchange_price_subtotal_ieps')
    gif_tax_id_ieps = fields.Char(string='Taxes',compute='_gif_onchange_tax_id_ieps')

    @api.onchange('tax_id')
    def _gif_onchange_tax_id_ieps(self):
        for record in self:
            if len(record.tax_id) > 0:
                string_ieps = ""
                for tax in record.tax_id:
                    if 'IEPS' in tax.name:
                        continue
                    else:
                        string_ieps = string_ieps +' ' + tax.description or tax.name
                record.gif_tax_id_ieps = string_ieps
            else:
                record.gif_tax_id_ieps = False

    @api.onchange('price_subtotal','gif_SaleOrderIeps')
    def _gif_onchange_price_subtotal_ieps(self):
        for record in self:
            if record.price_subtotal != False:
                record.gif_price_subtotal_ieps = record.price_subtotal + record.gif_SaleOrderIeps
            else:
                record.gif_price_subtotal_ieps = 0
    

    @api.onchange('price_unit','gif_SaleOrderIeps')
    def _gif_onchange_price_unit_ieps(self):
        for record in self:
            if record.price_unit != False:
                record.gif_price_unit_ieps = (record.price_subtotal + record.gif_SaleOrderIeps) / record.product_uom_qty
            else:
                record.gif_price_unit_ieps = 0
    
    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine,self)._prepare_invoice_line()
        res['gif_AccountMoveIeps'] = self.gif_SaleOrderIeps
        return res

    @api.onchange('product_template_id')
    def _get_display_ol(self):
        for record in self:
            if record.order_id.gif_IepsDisplay == True:
                record.gif_IepsDisplayOL = True
            else:
                record.gif_IepsDisplayOL = False
    
    @api.depends('state', 'price_reduce', 'product_id', 'untaxed_amount_invoiced', 'qty_delivered', 'product_uom_qty')
    def _compute_untaxed_amount_to_invoice(self):
        """ Total of remaining amount to invoice on the sale order line (taxes excl.) as
                total_sol - amount already invoiced
            where Total_sol depends on the invoice policy of the product.

            Note: Draft invoice are ignored on purpose, the 'to invoice' amount should
            come only from the SO lines.
        """
        print('El otro')
        for line in self:
            amount_to_invoice = 0.0
            if line.state in ['sale', 'done']:
                # Note: do not use price_subtotal field as it returns zero when the ordered quantity is
                # zero. It causes problem for expense line (e.i.: ordered qty = 0, deli qty = 4,
                # price_unit = 20 ; subtotal is zero), but when you can invoice the line, you see an
                # amount and not zero. Since we compute untaxed amount, we can use directly the price
                # reduce (to include discount) without using `compute_all()` method on taxes.
                price_subtotal = 0.0
                uom_qty_to_consider = line.qty_delivered if line.product_id.invoice_policy == 'delivery' else line.product_uom_qty
                price_reduce = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                price_subtotal = price_reduce * uom_qty_to_consider
                if len(line.tax_id.filtered(lambda tax: tax.price_include)) > 0:
                    # As included taxes are not excluded from the computed subtotal, `compute_all()` method
                    # has to be called to retrieve the subtotal without them.
                    # `price_reduce_taxexcl` cannot be used as it is computed from `price_subtotal` field. (see upper Note)
                    print('El que le damos: ',line.gif_SaleOrderIeps)
                    price_subtotal = line.tax_id.compute_all(
                        price_reduce,
                        currency=line.order_id.currency_id,
                        quantity=uom_qty_to_consider,
                        product=line.product_id,
                        partner=line.order_id.partner_shipping_id,
                        ieps=line.gif_SaleOrderIeps,)['total_excluded']
                inv_lines = line._get_invoice_lines()
                if any(inv_lines.mapped(lambda l: l.discount != line.discount)):
                    # In case of re-invoicing with different discount we try to calculate manually the
                    # remaining amount to invoice
                    amount = 0
                    for l in inv_lines:
                        if len(l.tax_ids.filtered(lambda tax: tax.price_include)) > 0:
                            amount += l.tax_ids.compute_all(l.currency_id._convert(l.price_unit, line.currency_id, line.company_id, l.date or fields.Date.today(), round=False) * l.quantity)['total_excluded']
                        else:
                            amount += l.currency_id._convert(l.price_unit, line.currency_id, line.company_id, l.date or fields.Date.today(), round=False) * l.quantity

                    amount_to_invoice = max(price_subtotal - amount, 0)
                else:
                    amount_to_invoice = price_subtotal - line.untaxed_amount_invoiced

            line.untaxed_amount_to_invoice = amount_to_invoice

    @api.onchange('price_unit','product_uom_qty')
    def _onchange_price_unit_gif_ieps(self):
        for record in self:
            if record.product_template_id.gif_type_ieps != False:
                if record.product_template_id.gif_type_ieps == '2':
                    record.gif_SaleOrderIeps = record.product_template_id.gif_ieps_sale_fij * record.product_uom.ratio * record.product_uom_qty
                elif record.product_template_id.gif_type_ieps == '1':
                    for tax in record.tax_id:
                        tax_value = 0
                        if 'IEPS' in tax.name:
                            tax_value = tax.amount
                            break
                    record.gif_SaleOrderIeps = record.price_subtotal * (tax_value / 100)
                if 'USD' in record.order_id.pricelist_id.currency_id.name:
                    record.gif_SaleOrderIeps = record.gif_SaleOrderIeps / record.order_id.gif_own_inverse_currency
                # if record.gif_IepsDisplayOL == False:
                #     record.price_unit = record.price_unit + record.gif_SaleOrderIeps
                # for t in record.tax_id:
                #     if 'IEPS' in t.name and record.gif_IepsDisplayOL == False:
                #         try:
                #             record.write({'tax_id': [(3,t.id)]})
                #             # record.gif_SaleOrderIeps = 0
                #         except Exception as e:
                #             print('No borra por : ',e)
                    
            else:
                record.gif_SaleOrderIeps = 0
                
     
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','gif_SaleOrderIeps')
    def _compute_amount(self):
        """
    Compute the amounts of the SO line.
    """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id,ieps=line.gif_SaleOrderIeps)
            for ta in taxes.get('taxes',[]):
                if 'IEPS' in ta['name']:
                    ta['amount'] = line.gif_SaleOrderIeps
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            # if line.gif_SaleOrderIeps != 0 and line.gif_SaleOrderIeps != False:
            #     line['price_tax'] = line['price_tax'] + (line.gif_SaleOrderIeps - 1)
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
          
    # @api.onchange('gif_SaleOrderIeps')
    # def _onchange_gif_SaleOrderIeps(self):
    #     for record in self:
    #         record.price_subtotal = record.price_subtotal + record.gif_SaleOrderIeps
    
class GifSaleOrder(models.Model):   
    _inherit="sale.order"

    gif_IepsDisplay = fields.Boolean(string='DisplayFieldIEPS',compute='_gif_show_ieps')

    gif_tax_totals_json = fields.Char(compute='_compute_gif_tax_totals_json')

    @api.depends('order_line.tax_id', 'order_line.gif_price_unit_ieps', 'amount_total', 'amount_untaxed')
    def _compute_gif_tax_totals_json(self):
        def gif_compute_taxes(order_line):
            price = order_line.gif_price_unit_ieps * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            return order_line.tax_id._origin.gif_compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id,ieps=order_line.gif_SaleOrderIeps)

        account_move = self.env['account.move']
        for order in self:
            gif_subtotal = 0
            for line in order.order_line:
                gif_subtotal += line.gif_price_subtotal_ieps
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, gif_compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, gif_subtotal, order.currency_id)
            order.gif_tax_totals_json = json.dumps(tax_totals)

    @api.onchange('partner_id')
    def _gif_show_ieps(self):
        for record in self:
            if record.partner_id.id != False:
                if record.partner_id.gif_ieps_desglose == True:
                    record.gif_IepsDisplay = True
                else:
                    record.gif_IepsDisplay = False
            else:
                record.gif_IepsDisplay = False
 
    @api.onchange('order_line')
    def _ShowIeps(self):
        for record in self:
            for line in record.order_line:
                producto = self.env['product.template'].search([('id','=',line.product_template_id.id)])
                if producto.gif_ieps_type_sale == '%':
                    line.gif_SaleOrderIepsChar = str(producto.gif_ieps_value_sale)+' % ($ '+str(line.price_unit*(producto.gif_ieps_value_sale/100))+')'
                else:
                    line.gif_SaleOrderIepsChar = '$ '+str(producto.gif_ieps_value_sale)
    

    #Al cambio en el valor del cliente se obtiene el valor del campo gif_ieps_desglose para saber si se
    #desglosa en IEPS o no
    @api.onchange('partner_id')
    def _IepsDisplay(self):
        for record in self:
            display = self.env['res.partner'].search([('id','=',record.partner_id.id)]).gif_ieps_desglose
            print("DISPLAY: ",display)
            record.gif_IepsDisplay = display
            self = self.with_context(gif_IepsDisplay = display)
            self.order_line = self.order_line.with_context(gif_IepsDisplay = display)

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            print('Ultima oportunidad: ')
            return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id,ieps=order_line.gif_SaleOrderIeps)

        self._amount_all()
        account_move = self.env['account.move']
        for order in self:
            print('Aquí se da uno en el sale order: ',order.amount_total)
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            currency = order.currency_id
            tax_totals['allow_tax_edition'] = True
            order.tax_totals_json = json.dumps(tax_totals)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
 