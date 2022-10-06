from odoo import models,api,fields,_
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar'),('posted',)], ondelete={'to_approve': 'set default'}, string="Status", index=True, readonly=True, default='draft')

    is_admin_office_accountform_purchase = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_primary_accountform_purchase = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_ben_dis_accountform_purchase = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_associated_accountform_purchase = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_insume_accountform_purchase = fields.Boolean(compute='_is_approve_account', default=False)

    is_admin_office_accountform_sale = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_primary_accountform_sale = fields.Boolean(compute='_is_approve_account', default=False)
    is_admin_ben_dis_accountform_sale = fields.Boolean(compute='_is_approve_account', default=False)

    purchase_pf = fields.Float(default=0,compute='_calculate_purchase')
    purchase_pp = fields.Float(default=0,compute='_calculate_purchase')
    sale_dis = fields.Float(default=0,compute='_calculate_sale')

    account_current_currency = fields.Float(default=0.0,compute="_calculate_currency_account_sa",store=True)
    account_current_inverse_currency = fields.Float(default=0.0,compute="_calculate_currency_account_sa")

    gif_temp_account = fields.Float(string="Tasa de Cambio",default=0.0,compute="_onchange_account_id_sale_autorization")
    

    @api.onchange('currency_id','account_current_inverse_currency','date')
    def _onchange_account_id_sale_autorization(self):
        print('Aquí se dice que cambia')
        for record in self:
            try:
                if record.gif_own_currency_check_account == True and record.gif_own_inverse_currency_account != 0:
                    record.account_current_currency = record.currency_id.rate
                    record.gif_temp_account = record.gif_own_inverse_currency_account
                else:
                    record.account_current_currency = record.currency_id.rate
                    record.gif_temp_account = record.currency_id.inverse_rate
            except:
                record.account_current_currency = record.currency_id.rate
                record.gif_temp_account = record.currency_id.inverse_rate
    
    @api.onchange('account_current_inverse_currency')
    def _onchange_account_current_inverse_currency_account_sa(self):
        try:
            self.gif_temp_account = self.gif_own_inverse_currency_account
        except:
            self.gif_temp_account = self.currency_id.inverse_rate
    

    @api.depends('account_current_currency','account_current_inverse_currency','date')
    def _calculate_currency_account_sa(self):
        for record in self:
            try: 
                if record.gif_own_currency_check_purchase ==True:
                    record.account_current_inverse_currency = record.gif_own_inverse_currency_account
                elif record.currency_id.inverse_rate != 0:
                    record.account_current_currency = record.currency_id.rate
                    record.account_current_inverse_currency = record.currency_id.inverse_rate
                else:
                    record.account_current_currency = 1
                    record.account_current_inverse_currency = 1
            except:
                if record.currency_id.inverse_rate != 0:
                    record.account_current_currency = record.currency_id.rate
                    record.account_current_inverse_currency = record.currency_id.inverse_rate
                else:
                    record.account_current_currency = 1
                    record.account_current_inverse_currency = 1

    def _calculate_sale(self):
        sale_price = 1
        for record in self:
            for line in record.invoice_line_ids:
                if record.type_of_sale:
                    if line.product_id.partners_details:
                        for partner in line.product_id.partners_details:
                            if partner.partner.name == record.partner_id.name:
                                sale_price = partner.partner_price
                    else:
                        sale_price = line.product_id.list_price
                    record.sale_dis = ((100 - line.product_id.porcentaje_ventas)/100 * sale_price)
                else:
                    record.sale_dis = 0
    
    def _calculate_purchase(self):
        uncalculated_purchase = 3
        for record in self:
            for line in record.invoice_line_ids:
                if record.type_of_purchase:
                    if line.product_id.partners_details_purchase:
                        for partner in line.product_id.partners_details_purchase:
                            if record.partner_id.name == partner.partner_purchase.name:
                                uncalculated_purchase = partner.partner_price_purchase
                    else:
                        uncalculated_purchase = line.product_id.standard_price
                    if line.product_id.descount_selector == "1":
                        record.purchase_pf = uncalculated_purchase + line.product_id.d_f
                        record.purchase_pp = 0
                    elif line.product_id.descount_selector == "2":
                        record.purchase_pf = 0
                        record.purchase_pp = ((line.product_id.d_p/100)* uncalculated_purchase )+ uncalculated_purchase
                else:
                    record.purchase_pf = 0
                    record.purchase_pp = 0
    
    def _is_approve_account(self):
        for record in self:
            user_group_ap = []
            add_user = self.env.uid
            groups_ap = self.env['res.groups'].search([('name','ilike','Validador')])
            for grupo_ap in groups_ap:
                if add_user in grupo_ap.users.ids:
                    user_group_ap.append(grupo_ap.name)
            if user_group_ap:
                for user_ap in user_group_ap:
                    if record.is_primary_accountform_purchase:
                        if 'Validador Transacciones Egreso Productos Primarios' in user_ap:
                            record.is_admin_primary_accountform_purchase = True
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                    elif record.is_office_accountform_purchase:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user_ap:
                            record.is_admin_office_accountform_purchase = True
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                    elif record.is_ben_dis_accountform_purchase:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user_ap:
                            record.is_admin_ben_dis_accountform_purchase = True
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                    elif record.is_insume_accountform_purchase:
                        if 'Validador Transacciones Egreso Productos Insumos' in user_ap:
                            record.is_admin_insume_accountform_purchase = True
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_ben_dis_accountform_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                    elif record.is_associated_accountform_purchase:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user_ap:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = True
                            record.is_admin_insume_accountform_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_purchase = False
                            record.is_admin_primary_accountform_purchase = False
                            record.is_admin_office_accountform_purchase = False
                            record.is_admin_associated_accountform_purchase = False
                            record.is_admin_insume_accountform_purchase = False
                    else:
                        record.is_admin_ben_dis_accountform_purchase = False
                        record.is_admin_primary_accountform_purchase = False
                        record.is_admin_office_accountform_purchase = False
                        record.is_admin_associated_accountform_purchase = False
                        record.is_admin_insume_accountform_purchase = False
            else:
                record.is_admin_ben_dis_accountform_purchase = False
                record.is_admin_primary_accountform_purchase = False
                record.is_admin_office_accountform_purchase = False
                record.is_admin_associated_accountform_purchase = False
                record.is_admin_insume_accountform_purchase = False

            user_group_as = []
            add_user = self.env.uid
            groups_as = self.env['res.groups'].search([('name','ilike','Validador')])
            for grupo_as in groups_as:
                if add_user in grupo_as.users.ids:
                    user_group_as.append(grupo_as.name)
            if user_group_as:
                for user_as in user_group_as:
                    if record.is_primary_accountform_sale:
                        if 'Validador Transacciones Ingreso Productos Primarios' in user_as:
                            record.is_admin_primary_accountform_sale = True
                            record.is_admin_office_accountform_sale = False
                            record.is_admin_ben_dis_accountform_sale = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_sale = False
                            record.is_admin_primary_accountform_sale = False
                            record.is_admin_office_accountform_sale = False
                    elif record.is_office_accountform_sale:
                        if 'Validador Transacciones Ingreso Productos de Oficina' in user_as:
                            record.is_admin_office_accountform_sale = True
                            record.is_admin_primary_accountform_sale = False
                            record.is_admin_ben_dis_accountform_sale = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_sale = False
                            record.is_admin_primary_accountform_sale = False
                            record.is_admin_office_accountform_sale = False
                    elif record.is_ben_dis_accountform_sale:
                        if 'Validador Transacciones Ingreso Descuentos y Beneficios' in user_as:
                            record.is_admin_ben_dis_accountform_sale = True
                            record.is_admin_primary_accountform_sale = False
                            record.is_admin_office_accountform_sale = False
                            break
                        else:
                            record.is_admin_ben_dis_accountform_sale = False
                            record.is_admin_primary_accountform_sale = False
                            record.is_admin_office_accountform_sale = False
                    else:
                        record.is_admin_ben_dis_accountform_sale = False
                        record.is_admin_primary_accountform_sale = False
                        record.is_admin_office_accountform_sale = False
            else:
                record.is_admin_ben_dis_accountform_sale = False
                record.is_admin_primary_accountform_sale = False
                record.is_admin_office_accountform_sale = False

    def action_post(self):
        try:
            go_to_approve_account = False
            if self.invoice_origin:
                sales = self.env['sale.order'].search([('name','=',self.invoice_origin)])
                purchases = self.env['purchase.order'].search([('name','=',self.invoice_origin)])
                for record in self:
                    for line in record.invoice_line_ids:
                        precio = line.price_unit
                        if record.type_of_purchase:
                            if purchases:
                                for p_line in purchases.order_line:
                                    if precio == p_line.price_unit:
                                        pass
                                    else:
                                        if record.is_primary_accountform_purchase and record.is_admin_primary_accountform_purchase:
                                            pass
                                        elif record.is_office_accountform_purchase and record.is_admin_office_accountform_purchase:
                                            pass
                                        elif record.is_ben_dis_accountform_purchase and record.is_admin_ben_dis_accountform_purchase:
                                            pass
                                        elif record.is_associated_accountform_purchase and record.is_admin_associated_accountform_purchase:
                                            pass
                                        elif record.is_insume_accountform_purchase and record.is_admin_insume_accountform_purchase:
                                            pass
                                        else:
                                            go_to_approve_account = True
                        elif record.type_of_sale:
                            if sales:
                                for s_line in sales.order_line:
                                    if precio == s_line.price_unit:
                                        pass
                                    else:
                                        if record.is_primary_accountform_sale and record.is_admin_primary_accountform_sale:
                                            pass
                                        elif record.is_office_accountform_sale and record.is_admin_office_accountform_sale:
                                            pass
                                        elif record.is_ben_dis_accountform_sale and record.is_admin_ben_dis_accountform:
                                            pass
                                        else:
                                            go_to_approve_account = True
            else:
                for record in self:
                    if record.type_of_purchase:
                        for line in record.invoice_line_ids:
                            precio = line.price_unit
                            for detail in line.product_id.partners_details_purchase:
                                if self.partner_id.name == detail.partner_purchase.name:
                                    if precio == detail.partner_price_purchase:
                                        pass
                                    else:
                                        if record.is_primary_accountform_purchase and record.is_admin_primary_accountform_purchase:
                                            pass
                                        elif record.is_office_accountform_purchase and record.is_admin_office_accountform_purchase:
                                            pass
                                        elif record.is_ben_dis_accountform_purchase and record.is_admin_ben_dis_accountform_purchase:
                                            pass
                                        elif record.is_associated_accountform_purchase and record.is_admin_associated_accountform_purchase:
                                            pass
                                        elif record.is_insume_accountform_purchase and record.is_admin_insume_accountform_purchase:
                                            pass
                                        else:
                                            go_to_approve_account = True
                    elif record.type_of_sale:
                        print('Es una venta')
                        for line in record.invoice_line_ids:
                            precio_s = line.price_unit
                            for detail_s in line.product_id.partners_details:
                                if self.partner_id.name == detail_s.partner.name:
                                    if precio_s == detail_s.partner_price:
                                        pass
                                    else:
                                        if record.is_primary_accountform_sale and record.is_admin_primary_accountform_sale:
                                            pass
                                        elif record.is_office_accountform_sale and record.is_admin_office_accountform_sale:
                                            pass
                                        elif record.is_ben_dis_accountform_sale and record.is_admin_ben_dis_accountform:
                                            pass
                                        else:
                                            go_to_approve_account = True
            if go_to_approve_account == True:
                record.state = 'to_approve'
            elif go_to_approve_account == False:
                print(line.product_uom_id.name)
                res = super(AccountMove, self).action_post()
                return res
        except Exception as e:
            print('Error: ',e)

    def authorize_account_primary_purchase(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_office_purchase(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_insume_purchase(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_associated_purchase(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_ben_dis_purchase(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_primary_sale(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_office_sale(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def authorize_account_ben_dis_sale(self):
        for record in self:
            res = super(AccountMove, self).action_post()
            return res

    def go_back_account(self):
        for record in self:
            record.state = 'draft'


class AccountMoveOrderLine(models.Model):
    _inherit = 'account.move.line'

    gif_difference_account = fields.Float(string="Cantidad",compute="_is_different_account_sa",default=0.0)
    gif_is_different_account = fields.Boolean(string='Vario',default=False,compute="_is_different_account_sa")
    
    @api.onchange('product_id')
    def _onchange_product_id_raise_error_if_not(self):
        for record in self:
            if record.product_id.name == False or record.product_id.detailed_type != 'product':
                gif_pasa = True
                pass
            else:
                if record.move_id.move_type in ('out_invoice','out_refund','out_receipt'):
                    user = 'Cliente'
                    if record.product_id.partners_details:
                        for partner in record.product_id.partners_details:
                            if record.move_id.partner_id.name == partner.partner.name:
                                gif_pasa = True
                                break
                            else:
                                gif_pasa = False
                    else:
                        gif_pasa = False
                elif record.move_id.move_type in ('in_invoice','in_refund','in_receipt'):
                    user = 'Proveedor'
                    if record.product_id.partners_details_purchase:
                        for partner in record.product_id.partners_details_purchase:
                            if record.move_id.partner_id.name == partner.partner_purchase.name:
                                gif_pasa = True
                                break
                            else:
                                gif_pasa = False
                    else:
                        gif_pasa = False
            if gif_pasa == False:
                record.product_id = None
                string = 'Este ' + user + ' no tiene precios asignados a este producto.'
                raise UserError(_(string))
            else:
                pass


    @api.onchange('product_uom_id')
    def onchange_product_id_changeprice(self):
        for record in self:
            if record.move_id.type_of_sale:
                if record.product_id.partners_details:
                    for partner in record.product_id.partners_details:
                        if record.move_id.partner_id.name in partner.partner.name:
                            record.price_unit = partner.partner_price
            elif record.move_id.type_of_purchase:
                if record.product_id.partners_details_purchase:
                    for partner in record.product_id.partners_details_purchase:
                        if record.move_id.partner_id.name in partner.partner_purchase.name:
                            record.price_unit = partner.partner_price_purchase
            if record.move_id.gif_temp_account > 0:
                record.price_unit = record.price_unit / record.move_id.gif_temp_account

    @api.onchange('name')
    def onchange_name_changeprice(self):
        for record in self:
            if record.move_id.type_of_sale:
                if record.product_id.partners_details:
                    for partner in record.product_id.partners_details:
                        if record.move_id.partner_id.name in partner.partner.name:
                            record.price_unit = partner.partner_price
                            record.product_uom_id = partner.partner_uom
            elif record.move_id.type_of_purchase:
                if record.product_id.partners_details_purchase:
                    for partner in record.product_id.partners_details_purchase:
                        if record.move_id.partner_id.name in partner.partner_purchase.name:
                            record.price_unit = partner.partner_price_purchase
                            record.product_uom_id = partner.partner_uom_purchase
            if record.move_id.gif_temp_account > 0:
                record.price_unit = record.price_unit / record.move_id.gif_temp_account

    @api.onchange('product_id')
    def onchange_quantity_changeprice(self):
        for record in self:
            if record.move_id.type_of_sale:
                if record.product_id.partners_details:
                    for partner in record.product_id.partners_details:
                        if record.move_id.partner_id.name in partner.partner.name:
                            record.price_unit = partner.partner_price
            elif record.move_id.type_of_purchase:
                if record.product_id.partners_details_purchase:
                    for partner in record.product_id.partners_details_purchase:
                        if record.move_id.partner_id.name in partner.partner_purchase.name:
                            print('Se le asigna el precio de compra: ')
                            record.price_unit = partner.partner_price_purchase
                            print(record.price_unit)
            if record.move_id.gif_temp_account > 0:
                record.price_unit = record.price_unit / record.move_id.gif_temp_account

    @api.onchange('price_unit')
    def _is_different_account_sa(self):
        for record in self:
            record.gif_is_different_account = False
            record.gif_difference_account = 0.0
            if record.move_id.type_of_sale:
                for partner in record.product_id.partners_details:
                    if record.move_id.partner_id.name == partner.partner.name:
                        if record.move_id.gif_temp_account == 0:
                            pp_difference = 1
                        elif record.move_id.gif_temp_account != 0:
                            pp_difference = record.move_id.gif_temp_account
                        if record.price_unit != (partner.partner_price/pp_difference):
                            record.gif_difference_account = record.price_unit - (partner.partner_price / pp_difference)
                        else:
                            record.gif_difference_account = 0.0
                        if record.gif_difference_account == 0:
                            record.gif_is_different_account = False
                        elif round(record.gif_difference_account,2) != 0:
                            record.gif_is_different_account = True
            elif record.move_id.type_of_purchase:
                for partner_p in record.product_id.partners_details_purchase:
                    if record.move_id.partner_id.name == partner_p.partner_purchase.name:
                        if record.move_id.gif_temp_account == 0:
                            pp_difference = 1
                        elif record.move_id.gif_temp_account != 0:
                            pp_difference = record.move_id.gif_temp_account
                        if record.price_unit != (partner_p.partner_price_purchase/pp_difference):
                            record.gif_difference_account = record.price_unit -(partner_p.partner_price_purchase / pp_difference) 
                        else:
                            record.gif_difference_account = 0.0
                        if record.gif_difference_account == 0:
                            record.gif_is_different_account = False
                        elif round(record.gif_difference_account,2) != 0:
                            record.gif_is_different_account = True


