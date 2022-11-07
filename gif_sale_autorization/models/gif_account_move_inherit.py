from odoo import models,api,fields, exceptions,_
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

    gif_temp_account = fields.Float(string="Tasa de Cambio",default=0.0,compute="_onchange_account_id_sale_autorization")
    

    @api.onchange('currency_id','date')
    def _onchange_account_id_sale_autorization(self):
        '''
            En está función se asigna el valor del tipo de moneda con el que va a trabajar, se hizo así porque
            hay un desarrollo que es poner la tasa manual (gif_chance_currency).
        '''
        for record in self:
            try:
                if record.gif_own_currency_check_account == True and record.gif_own_inverse_currency_account != 0:
                    record.gif_temp_account = record.gif_own_inverse_currency_account
                else:
                    record.gif_temp_account = record.currency_id.inverse_rate
            except:
                record.gif_temp_account = record.currency_id.inverse_rate
    
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
        '''
            Está es la función que aplica el botón de confirmar, aquí pasa por las condiciones
            para ver si se va al estado de aprobación o no. Las cuales son:
                -Si el precio unitario es diferente al precio que tiene el cliente/proveedor en su tabla,
                se irá a aprobación, a excepción que sea el admin.
        '''
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
                res = super(AccountMove, self).action_post()
                return res
        except Exception as e:
            raise UserError(_(e))

    
    #Dependiendo de la categoria se mostrará un boton diferente, todos hacen la acción de confirmar.

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
        #Este es el botón que lo regresa al estado de borrador cuando está por aprobar.
        for record in self:
            record.state = 'draft'


class AccountMoveOrderLine(models.Model):
    _inherit = 'account.move.line'

    gif_difference_account = fields.Float(string="Cantidad",compute="_is_different_account_sa",default=0.0)
    gif_is_different_account = fields.Boolean(string='Vario',default=False,compute="_is_different_account_sa")
    
    @api.onchange('product_id')
    def _onchange_product_id_raise_error_if_not(self):
        #Validación para ver si el producto tiene precio con el cliente/proveedor.
        for record in self:
            if record.product_id.name == False or record.product_id.detailed_type != 'product':
                gif_pasa = True
                pass
            else:
                if record.move_id.move_type in ('out_invoice','out_refund','out_receipt'):
                    user = 'Cliente'
                    if record.product_id.partners_details:
                        for partner in record.product_id.partners_details:
                            if record.move_id.partner_id.name == partner.partner.name and record.move_id.currency_id.name == partner.currency_sale.name:
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
                            if record.move_id.partner_id.name == partner.partner_purchase.name and record.move_id.currency_id.name == partner.currency_purchase.name:
                                gif_pasa = True
                                break
                            else:
                                gif_pasa = False
                    else:
                        gif_pasa = False
            if gif_pasa == False:
                record.product_id = None
                string = 'Este ' + user + ' no tiene precios asignados a este producto.'
                raise exceptions.UserError(_(string))
            else:
                pass


    @api.onchange('product_uom_id')
    def onchange_product_id_changeprice(self):
        '''
            Aquí se asigna el precio unitario en base a la tabla que se tienen en los productos.
        '''
        for record in self:
            if record.move_id.type_of_sale:
                if record.product_id.partners_details:
                    for partner in record.product_id.partners_details:
                        if record.move_id.partner_id.name in partner.partner.name and record.move_id.currency_id.name == partner.currency_sale.name:
                            record.price_unit = partner.partner_price
                        # if record.move_id.gif_temp_account > 0:
                        #     if partner.currency_sale:
                        #         if partner.currency_sale.name == 'USD' and record.move_id.currency_id.name == 'MXN':
                        #             if record.move_id.gif_temp_account != 1.0:
                        #                 record.price_unit = record.price_unit * record.move_id.gif_temp_account
                        #             else:
                        #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                        #                 if divisa:
                        #                     record.price_unit = record.price_unit * divisa.rate_ids[0].inverse_company_rate
                        #         elif partner.currency_sale.name == 'MXN' and record.move_id.currency_id.name == 'USD':
                        #             if record.move_id.gif_temp_account != 1.0:
                        #                 record.price_unit = record.price_unit / record.move_id.gif_temp_account
                        #             else:
                        #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                        #                 if divisa:
                        #                     record.price_unit = record.price_unit / divisa.rate_ids[0].inverse_company_rate
                        #         else:
                        #             record.price_unit = record.price_unit
            
            elif record.move_id.type_of_purchase:
                if record.product_id.partners_details_purchase:
                    for partner in record.product_id.partners_details_purchase:
                        if record.move_id.partner_id.name in partner.partner_purchase.name and record.move_id.currency_id.name == partner.currency_purchase.name:
                            record.price_unit = partner.partner_price_purchase
                        # if record.move_id.gif_temp_account > 0:
                        #     if partner.currency_purchase:
                        #         if partner.currency_purchase.name == 'USD' and record.move_id.currency_id.name == 'MXN':
                        #             if record.move_id.gif_temp_account != 1.0:
                        #                 record.price_unit = record.price_unit * record.move_id.gif_temp_account
                        #             else:
                        #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                        #                 if divisa:
                        #                     record.price_unit = record.price_unit * divisa.rate_ids[0].inverse_company_rate
                        #         elif partner.currency_purchase.name == 'MXN' and record.move_id.currency_id.name == 'USD':
                        #             if record.move_id.gif_temp_account != 1.0:
                        #                 record.price_unit = record.price_unit / record.move_id.gif_temp_account
                        #             else:
                        #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                        #                 if divisa:
                        #                     record.price_unit = record.price_unit / divisa.rate_ids[0].inverse_company_rate
                        #         else:
                        #             record.price_unit = record.price_unit
            

    @api.onchange('name')
    def onchange_name_changeprice(self):
        '''
            Aquí se asigna el precio unitario en base a la tabla que se tienen en los productos.
            También se calcula la unidad de medida.
            ¿Por qué en dos funciones diferentes? No lo sé, Odoo de otra forma no lo cambiaba o lo hacia mal.
        '''
        for record in self:
            if record.move_id.type_of_sale:
                if record.product_id.partners_details:
                    for partner in record.product_id.partners_details:
                        if record.move_id.partner_id.name in partner.partner.name and record.move_id.currency_id.name == partner.currency_sale.name:
                            record.price_unit = partner.partner_price
                            record.product_uom_id = partner.partner_uom
            elif record.move_id.type_of_purchase:
                if record.product_id.partners_details_purchase:
                    for partner in record.product_id.partners_details_purchase:
                        if record.move_id.partner_id.name in partner.partner_purchase.name and record.move_id.currency_id.name == partner.currency_purchase.name:
                            record.price_unit = partner.partner_price_purchase
                            record.product_uom_id = partner.partner_uom_purchase

    @api.onchange('price_unit')
    def _is_different_account_sa(self):
        '''
            Esta es la función que dice si el precio varia con la cantidad que se encuentra en la tabla.
        '''
        for record in self:
            record.gif_is_different_account = False
            record.gif_difference_account = 0.0
            if record.move_id.type_of_sale:
                for partner in record.product_id.partners_details:
                    if record.move_id.partner_id.name == partner.partner.name and record.move_id.currency_id.name == partner.currency_sale.name:
                        if record.price_unit != (partner.partner_price):
                            # if record.move_id.gif_temp_account != 0:
                            #     if partner.currency_sale:
                            #         if record.move_id.currency_id.name == 'MXN' and partner.currency_sale.name == 'USD':
                            #             if record.move_id.gif_temp_account != 1.0:
                            #                 record.gif_difference_account = record.price_unit - (partner.partner_price * record.move_id.gif_temp_account)
                            #             else:
                            #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                            #                 if divisa:
                            #                     record.gif_difference_account = record.price_unit - (partner.partner_price * divisa.rate_ids[0].inverse_company_rate)
                            #         elif record.move_id.currency_id.name == 'USD' and partner.currency_sale.name == 'MXN':
                            #             if record.move_id.gif_temp_account != 1.0:
                            #                 record.gif_difference_account = record.price_unit - (partner.partner_price / record.move_id.gif_temp_account)
                            #             else:
                            #                 divisa = divisa = self.env['res.currency'].search([('name','=','USD')])
                            #                 if divisa:
                            #                     record.gif_difference_account = record.price_unit - (partner.partner_price / divisa.rate_ids[0].inverse_company_rate)
                            #         else:
                            record.gif_difference_account = record.price_unit - partner.partner_price
                            #     else:
                            #         record.gif_difference_account = record.price_unit - (partner.partner_price / record.move_id.gif_temp_account)
                            # else:
                            #     record.gif_difference_account = record.price_unit - partner.partner_price
                        else:
                            record.gif_difference_account = 0.0
                if record.gif_difference_account == 0:
                    record.gif_is_different_account = False
                elif round(record.gif_difference_account,2) != 0:
                    record.gif_is_different_account = True
            elif record.move_id.type_of_purchase:
                for partner_p in record.product_id.partners_details_purchase:
                    if record.move_id.partner_id.name == partner_p.partner_purchase.name and record.move_id.currency_id.name == partner_p.currency_purchase.name:
                        if record.price_unit != (partner_p.partner_price_purchase):
                            # if record.move_id.gif_temp_account != 0:
                            #     if partner_p.currency_purchase:
                            #         if record.move_id.currency_id.name == 'MXN' and partner_p.currency_purchase.name == 'USD':
                            #             if record.move_id.gif_temp_account != 1.0:
                            #                 record.gif_difference_account = record.price_unit - (partner_p.partner_price_purchase * record.move_id.gif_temp_account)
                            #             else:
                            #                 divisa = self.env['res.currency'].search([('name','=','USD')])
                            #                 if divisa:
                            #                     record.gif_difference_account = record.price_unit - (partner_p.partner_price_purchase * divisa.rate_ids[0].inverse_company_rate)
                            #         elif record.move_id.currency_id.name == 'USD' and partner_p.currency_purchase.name == 'MXN':
                            #             if record.move_id.gif_temp_account != 1.0:
                            #                 record.gif_difference_account = record.price_unit - (partner_p.partner_price_purchase / record.move_id.gif_temp_account)
                            #             else:
                            #                 divisa = divisa = self.env['res.currency'].search([('name','=','USD')])
                            #                 if divisa:
                            #                     record.gif_difference_account = record.price_unit - (partner_p.partner_price_purchase / divisa.rate_ids[0].inverse_company_rate)
                            #         else:
                            record.gif_difference_account = record.price_unit - partner_p.partner_price_purchase
                            break
                        #             break
                        #         else:
                        #             record.gif_difference_account = record.price_unit - (partner_p.partner_price_purchase / record.move_id.gif_temp_account)
                        #     else:
                        #         record.gif_difference_account = record.price_unit - partner_p.partner_price_purchase 
                        # else:
                        #     record.gif_difference_account = 0.0
                if record.gif_difference_account == 0:
                    record.gif_is_different_account = False
                elif round(record.gif_difference_account,2) != 0:
                    record.gif_is_different_account = True


