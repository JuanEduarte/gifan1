from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar'),('sent',)], string="Status", index=True, readonly=True, default='draft')
    is_approve = fields.Boolean(compute='_is_approve')
    is_admin_office_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_primary_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_ben_dis_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_discount_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_associated_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)
    is_admin_insume_purchase = fields.Boolean(compute='_is_approve_purchase', default=False)

    is_primary_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_insume_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_office_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_associated_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_ben_dis_purchaseform = fields.Boolean(compute='_purchaseform_calculate')
    is_discount_purchaseform = fields.Boolean(compute='_purchaseform_calculate')

    gif_purchase_currency = fields.Float(default=0.0, string="Tasa Técnica")
    gif_purchase_inverse_currency = fields.Float(default=0.0, string="MXN por Unidad",compute="_calculate_currency_purchase_sa",store=True)

    gif_real_validator = fields.Float(default=0.0,compute="_gif_calculate_real_validator_ev")
    gif_temp_validator = fields.Float(default=0.0,compute="_onchange_currency_id_purchase_sa",string="Tasa de cambio")

    # gif_should_block = fields.Boolean(default=False)
    
    

    @api.onchange('currency_id')
    def _onchange_currency_id_purchase_sa(self):
        '''
            En está función se asigna el valor del tipo de moneda con el que va a trabajar, se hizo así porque
            hay un desarrollo que es poner la tasa manual (gif_chance_currency).
        '''
        for record in self:
            record.gif_temp_validator = record.currency_id.inverse_rate
    

    @api.depends('gif_purchase_inverse_currency')
    def _calculate_currency_purchase_sa(self):
        '''
            Realmente este campo no se ocupa, pero no lo podemos eliminar porque está en la vista.
            Y si lo eliminamos de la vista tendriamos que desinstalar el desarrollo y a este altura eso
            ya no se puede.
        '''
        for record in self:
            if record.currency_id.inverse_rate != 0:
                record.gif_purchase_inverse_currency = record.currency_id.inverse_rate
            else:
                record.gif_purchase_inverse_currency = 1
    
    def _gif_calculate_real_validator_ev(self):
        '''
            Realmente este campo no se ocupa, pero no lo podemos eliminar porque está en la vista.
            Y si lo eliminamos de la vista tendriamos que desinstalar el desarrollo y a este altura eso
            ya no se puede.
        '''
        if self.gif_purchase_inverse_currency != 0:
            self.gif_real_validator = self.gif_purchase_inverse_currency
        else:
            self.gif_real_validator = 1
    
    def _purchaseform_calculate(self):
        '''
            Se computa que tipo de compra es
        '''
        for record in self:
            record.is_discount_purchaseform = False
            if record.tipificacion_compra.id == 1:
                record.is_primary_purchaseform = True
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 2:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = True
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 3:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = True
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            elif record.tipificacion_compra.id == 4:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = True
            elif record.tipificacion_compra.id == 5:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = True
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False
            else:
                record.is_primary_purchaseform = False
                record.is_office_purchaseform = False
                record.is_ben_dis_purchaseform = False
                record.is_insume_purchaseform = False
                record.is_associated_purchaseform = False

    def _is_approve_purchase(self):
        '''
            Funcion que comprueba si el usuario es administrador para ese tipo de compra
        '''
        for record in self:
            user_group = []
            add_user = self.env.uid
            groups_i = self.env['res.groups'].search([('name','ilike','Validador')])
            for grupo in groups_i:
                if add_user in grupo.users.ids:
                    user_group.append(grupo.name)
            if user_group:
                for user in user_group:
                    if record.is_primary_purchaseform:
                        if 'Validador Transacciones Egreso Productos Primarios' in user:
                            record.is_admin_primary_purchase = True
                            record.is_admin_office_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_discount_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_office_purchaseform:
                        if 'Validador Transacciones Egreso Productos de Oficina' in user:
                            record.is_admin_office_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_ben_dis_purchaseform:
                        if 'Validador Transacciones Egreso Descuentos y Beneficios' in user:
                            record.is_admin_ben_dis_purchase = True
                            record.is_admin_discount_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_insume_purchaseform:
                        if 'Validador Transacciones Egreso Productos Insumos' in user:
                            record.is_admin_insume_purchase = True
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                    elif record.is_associated_purchaseform:
                        if 'Validador Transacciones Egreso Gastos Asociados' in user:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = True
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
                            break
                        else:
                            record.is_admin_ben_dis_purchase = False
                            record.is_admin_primary_purchase = False
                            record.is_admin_office_purchase = False
                            record.is_admin_associated_purchase = False
                            record.is_admin_insume_purchase = False
                            record.is_admin_discount_purchase = False
            else:
                record.is_admin_discount_purchase = False
                record.is_admin_ben_dis_purchase = False
                record.is_admin_primary_purchase = False
                record.is_admin_office_purchase = False
                record.is_admin_associated_purchase = False
                record.is_admin_insume_purchase = False

    def button_confirm(self):
        for record in self:
            go_to_approve = False
            for line in record.order_line:
                temp = line.price_unit
                if line.product_template_id.descount_selector == "1":
                    fixed = line.d_f_id_purchases
                    porc = 0
                    if temp > fixed:
                        if temp >= 0:
                            if record.is_primary_purchaseform and record.is_admin_primary_purchase:
                                pass
                            elif record.is_office_purchaseform and record.is_admin_office_purchase:
                                pass
                            elif record.is_ben_dis_purchaseform and record.is_admin_ben_dis_purchase:
                                pass
                            elif record.is_associated_purchaseform and record.is_admin_associated_purchase:
                                pass
                            elif record.is_insume_purchaseform and record.is_admin_insume_purchase:
                                pass
                            else:
                                go_to_approve = True
                        else:
                            raise exceptions.UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
                    else:
                        pass
                elif line.product_template_id.descount_selector == "2":
                    porc = line.d_p_id_purchases
                    fixed = 0
                    if  temp > porc:
                        if temp>= 0:
                            if record.is_primary_purchaseform and record.is_admin_primary_purchase:
                                pass
                            elif record.is_office_purchaseform and record.is_admin_office_purchase:
                                pass
                            elif record.is_ben_dis_purchaseform and record.is_admin_ben_dis_purchase:
                                pass
                            elif record.is_associated_purchaseform and record.is_admin_associated_purchase:
                                pass
                            elif record.is_insume_purchaseform and record.is_admin_insume_purchase:
                                pass
                            else:
                                go_to_approve = True
                        else:
                            raise exceptions.UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
                    else:
                        pass
            if go_to_approve == True:
                record.state = 'to_approve'
            else:
                res = super(PurchaseOrder, self).button_approve()
                return res

    def authorize_purchase_primary(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_office(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_insume(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_associated(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res
    def authorize_purchase_ben_dis(self):
        for record in self:
            res = super(PurchaseOrder, self).button_approve()
            return res

    def go_back_purchase(self):
        for record in self:
            record.state="draft"

    @api.onchange('requisition_id')
    def _purchase_type_inherit_ps(self):
        for record in self:
            record.tipificacion_compra = record.requisition_id.tipificacion_requisition
            for line in record.order_line:
                if line.product_template_id.partners_details_purchase:
                    for p in line.product_template_id.partners_details_purchase:
                        if record.partner_id.name ==  p.partner_purchase.name:
                            line.product_uom = p.partner_uom_purchase

    # @api.onchange('partner_id')
    # def _onchange_partner_id_gsa(self):
    #     for record in self:
    #         if record.partner_id.id != False:
    #             if record.partner_id.gif_listprice == True:
    #                 record.gif_should_block = True
    #             else:
    #                 record.gif_should_block = False
    #         else:
    #             record.gif_should_block = False
    

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_template_id = fields.Many2one('product.template')
    d_p_id_purchases = fields.Float(compute='_compute_pp_purchases')
    d_f_id_purchases = fields.Float(compute='_compute_pf_purchases')

    gif_difference_purchase = fields.Float(string="Cantidad",default=0.0 ,compute='_is_difference_purchase_sa')
    gif_is_different_purchase = fields.Boolean(string="Varia",default=False,compute='_is_difference_purchase_sa')

    gif_block = fields.Boolean(compute='_gif_set_block')

    def _gif_set_block(self):
        for record in self:
            try:
                if self.order_line.gif_should_block == True:
                    record.gif_block = True
                else:
                    record.gif_block = False
            except:
                record.gif_block = False
    

    @api.constrains('product_template_id')
    @api.onchange('product_template_id')
    def _check_uom_and_product_gif(self):
        try:
            has_to_pass = False
            uom_pass = False
            for record in self:
                # record.gif_should_block = False
                if record.product_template_id.detailed_type != 'product':
                    uom_pass = True
                    has_to_pass = True
                else:
                    if record.product_template_id != False:
                        if record.product_template_id.partners_details_purchase:
                            for p in record.product_template_id.partners_details_purchase:
                                if record.order_id.partner_id.name in p.partner_purchase.name and record.order_id.currency_id.name == p.currency_purchase.name:
                                    has_to_pass = True
                                    if record.product_uom == False or record.product_uom == p.partner_uom_purchase:
                                        uom_pass = True
                                        break
                                    else:
                                        uom_pass = False
                                else:
                                    has_to_pass = False
                    else:
                        uom_pass = True
                        has_to_pass = True
        except Exception as e:
            print('Error 2: ',e)

    @api.onchange('price_unit')
    def _onchange_price_unit_gsa(self):
        price_block = False
        try:
            for record in self:
                # record.gif_should_block = False
                if record.product_template_id.detailed_type != 'product':
                    price_block = False
                else:
                    if record.price_unit != False:
                        if record.product_template_id.partners_details_purchase:
                            for p in record.product_template_id.partners_details_purchase:
                                if record.order_id.partner_id.name in p.partner_purchase.name and record.order_id.currency_id.name == p.currency_purchase.name and record.price_unit != p.partner_price_purchase:
                                    price_block = True
                                    break
                                else:
                                    price_block = False
                        # else:
                            # record.gif_should_block = True
                            # raise exceptions.ValidationError(_('Este producto no tiene proveedores asignados.'))
                    else:
                        price_block = False
            if price_block == True:
                raise exceptions.ValidationError('No puedes modificar el precio de este producto')
        except Exception as e:
            if price_block == True:
                raise ValidationError('No puedes modificar el precio de este producto')

    
    
    @api.onchange('product_template_id')
    def _onchange_product_template_id_reset_order_line_sa(self):
        for record in self:
            # record.gif_should_block = False
            if record.product_template_id.name == False or record.product_template_id.detailed_type != 'product':
                gif_pasa = True
                pass
            else:
                if record.product_template_id.partners_details_purchase:
                    for p in record.product_template_id.partners_details_purchase:
                        if (record.order_id.partner_id.name == p.partner_purchase.name or record.order_id.partner_id.name == p.partner_purchase.name) and record.order_id.currency_id.name == p.currency_purchase.name:
                            gif_pasa = True
                            break
                        else:
                            gif_pasa = False
                else:
                    gif_pasa = False
            if gif_pasa == False:
                record.product_template_id = None
            else:
                pass
    

    @api.onchange('product_uom')
    def _compute_pp_purchases(self):
        for record in self:
            if record.product_template_id.d_p < 0 or record.product_template_id.standard_price < 0:
                raise exceptions.UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
            else:
                if record.product_template_id.d_p > 100:
                    raise exceptions.UserError(_('El descuento porcentual no puede ser mayor a 100.'))
                else:
                    if record.product_template_id.partners_details_purchase:
                        for p in record.product_template_id.partners_details_purchase:
                            if (record.order_id.partner_id.name == p.partner_purchase.name or record.order_id.partner_id.name in p.partner_purchase.name) and  record.order_id.currency_id.name == p.currency_purchase.name:
                                if record.order_id.gif_temp_validator:
                                    cost = p.partner_price_purchase/record.order_id.gif_temp_validator
                                    currency_discount = record.product_template_id.d_p/record.order_id.gif_temp_validator
                                else:
                                    cost = p.partner_price_purchase
                                    currency_discount = record.product_template_id.d_p
                                record.d_p_id_purchases = ((currency_discount/100) * cost) + cost
                                break
                        



    @api.onchange('product_uom')
    def _compute_pf_purchases(self):
        for record in self:
            if record.product_template_id.d_f < 0 or record.product_template_id.standard_price < 0:
                raise exceptions.UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
            else:
                if record.product_template_id.partners_details_purchase:
                    for p in record.product_template_id.partners_details_purchase:
                        if (record.order_id.partner_id.name == p.partner_purchase.name or record.order_id.partner_id.name in p.partner_purchase.name) and  record.order_id.currency_id.name == p.currency_purchase.name:
                            if record.order_id.gif_temp_validator:
                                cost = p.partner_price_purchase/record.order_id.gif_temp_validator
                                record.d_f_id_purchases = cost + ((record.product_template_id.d_f)/record.order_id.gif_temp_validator)
                            else:
                                cost = p.partner_price_purchase
                                record.d_f_id_purchases = cost + record.product_template_id.d_f
                            break
                        



    @api.depends('product_template_id')
    def _give_ids(self):
        for record in self:
            record.d_p = record.product_template_id.d_p_id_purchases

    @api.onchange('product_uom')
    def product_purchase_change(self):
        for record in self:
            if record.order_id.requisition_id:
                pass
            else:
                coin_name = False
                for partner_purchase in record.product_template_id.partners_details_purchase:
                    if  (record.order_id.partner_id.name == partner_purchase.partner_purchase.name or record.order_id.partner_id.name in partner_purchase.partner_purchase.name) and record.order_id.currency_id.name == partner_purchase.currency_purchase.name:
                        record.product_uom = partner_purchase.partner_uom_purchase
                        record.price_unit = partner_purchase.partner_price_purchase
                        if record.product_uom == partner_purchase.partner_uom_purchase:
                            record.product_uom = None
                            record.product_uom = partner_purchase.partner_uom_purchase
                            record.price_unit = partner_purchase.partner_price_purchase
                            coin_name = partner_purchase.currency_purchase.name
                            break

    @api.onchange('product_qty')
    def _onchange_quantity_purchase_sale_autorization(self):
        try:
            if self.order_id.requisition_id:
                pass
            else:
                for line in self:
                    for partner_purchase in line.product_template_id.partners_details_purchase:
                        if  line.order_id.partner_id.name == partner_purchase.partner_purchase.name and line.order_id.currency_id.name == partner_purchase.currency_purchase.name:
                                line.product_uom = partner_purchase.partner_uom_purchase
                                line.price_unit = partner_purchase.partner_price_purchase
                                break
                    # if line.order_id.currency_id and line.order_id.gif_temp_validator != 0 and line.order_id.currency_id.name != partner_purchase.currency_purchase.name:
                    #     if line.order_id.currency_id.name != 'MXN' and partner_purchase.currency_purchase.name == 'MXN':
                    #         line.price_unit = line.price_unit / line.order_id.gif_temp_validator
                    #     else:
                    #         line.price_unit = line.price_unit * line.order_id.gif_temp_validator
        except:
            pass
  
    @api.onchange('price_unit')
    def _is_difference_purchase_sa(self):
        for record in self:
            try:
                if record.product_template_id.partners_details_purchase:
                    for p in record.product_template_id.partners_details_purchase:
                        if (record.order_id.partner_id.name == p.partner_purchase.name or record.order_id.partner_id.name in p.partner_purchase.name) and record.order_id.currency_id.name == p.currency_purchase.name:
                            if record.product_template_id.descount_selector == "2" or record.product_template_id.descount_selector == "1":
                                if record.price_unit != p.partner_price_purchase:
                                    record.gif_is_different_purchase = True
                                    record.gif_difference_purchase = record.price_unit - p.partner_price_purchase
                                    break
                                else:
                                    record.gif_is_different_purchase = False
                                    record.gif_difference_purchase = 0
                            else:
                                record.gif_difference_purchase = 0
                            break
                        else:
                            record.gif_difference_purchase = 0
                            record.gif_is_different_purchase = False
                    if record.gif_difference_purchase != 0:
                        record.gif_is_different_purchase = True
                    else:
                        record.gif_is_different_purchase = False
                else:
                    record.gif_difference_purchase = 0
                    record.gif_is_different_purchase = False
            except:
                record.gif_difference_purchase = 0
                record.gif_is_different_purchase = False