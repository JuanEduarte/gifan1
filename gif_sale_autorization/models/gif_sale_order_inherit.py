from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar'),('sent',)], string="Status", index=True, readonly=True, default='draft')
    is_approve = fields.Boolean(compute='_is_approve')
    is_admin_office = fields.Boolean(compute='_is_approve', default=False)
    is_admin_primary = fields.Boolean(compute='_is_approve', default=False)
    is_admin_ben_dis = fields.Boolean(compute='_is_approve', default=False)
    is_admin_discount = fields.Boolean(compute='_is_approve', default=False)
    is_primary_saleform = fields.Boolean(compute='_saleform_calculate')
    is_office_saleform = fields.Boolean(compute='_saleform_calculate')
    is_ben_dis_saleform = fields.Boolean(string='_saleform_calculate')
    
    gif_temp_sale = fields.Float(string="Tasa de cambio",default=0.0,compute="_onchange_pricelist_id_variable_exchange_sale")
    gif_real_sale = fields.Float(default=0.0,compute="_gif_calculate_real_sale_sa")


    gif_related_currency_sale = fields.Many2one(related='pricelist_id.currency_id', depends=["pricelist_id"] ,string='Tipo de cambio actual')
    gif_sale_currency = fields.Float(default=0.0, string="Tasa Técnica",compute="_calculate_currency_sale_sa")
    gif_sale_inverse_currency = fields.Float(default=0.0, string="MXN por Unidad",compute="_calculate_currency_sale_sa")
    
    @api.onchange('gif_temp_sale','pricelist_id','date_order')
    @api.depends('gif_sale_currency','gif_sale_inverse_currency')
    def _calculate_currency_sale_sa(self):
        for record in self:
            try: 
                if record.gif_own_currency_check_sale == True:
                    record.gif_sale_inverse_currency = record.gif_own_inverse_currency
                elif record.gif_related_currency_sale.inverse_rate != 0:
                    record.gif_sale_currency = record.gif_related_currency_sale.rate
                    record.gif_sale_inverse_currency = record.gif_temp_sale
                else:
                    record.gif_sale_currency = 1
                    record.gif_sale_inverse_currency = 1
            except:
                if record.gif_related_currency_sale.inverse_rate != 0:
                    record.gif_sale_currency = record.gif_related_currency_sale.rate
                    record.gif_sale_inverse_currency = record.gif_related_currency_sale.inverse_rate
                else:
                    record.gif_sale_currency = 1
                    record.gif_sale_inverse_currency = 1

    @api.onchange('pricelist_id','gif_sale_inverse_currency','date_order')
    def _onchange_pricelist_id_variable_exchange_sale(self):
        for record in self:
            try:
                if record.gif_own_currency_check_sale == True:
                    record.gif_temp_sale = record.gif_own_inverse_currency
                else:
                    record.gif_temp_sale = record.gif_related_currency_sale.inverse_rate
            except:
                if record.gif_sale_inverse_currency != 0 or record.pricelist_id.inverse_rate != 0:
                    record.gif_temp_sale = record.gif_sale_inverse_currency or record.pricelist_id.inverse_rate
        
    @api.onchange('tipificacion_venta')
    def _saleform_calculate(self):
        if self.tipificacion_venta.id == 1:
            self.is_primary_saleform = True
            self.is_office_saleform = False
            self.is_ben_dis_saleform = False
        elif self.tipificacion_venta.id == 2:
            self.is_primary_saleform = False
            self.is_office_saleform = True
            self.is_ben_dis_saleform = False
        elif self.tipificacion_venta.id == 3:
            self.is_primary_saleform = False
            self.is_office_saleform = False
            self.is_ben_dis_saleform = True
        else:
            self.is_primary_saleform = False
            self.is_office_saleform = False
            self.is_ben_dis_saleform = False

    def _is_approve(self):
        for record in self:
            user_group = []
            add_user = self.env.uid
            groups_i = self.env['res.groups'].search([('name','ilike','Validador')])
            for grupo in groups_i:
                if add_user in grupo.users.ids:
                    user_group.append(grupo.name)
            if user_group:
                for user in user_group:
                    if record.is_primary_saleform:
                        if 'Validador Transacciones Ingreso Productos Primarios' in user:
                            record.is_admin_primary = True
                            record.is_admin_office = False
                            record.is_admin_ben_dis = False
                            record.is_admin_discount = False
                            break
                        else:
                            record.is_admin_primary = False
                            record.is_admin_office = False
                            record.is_admin_ben_dis = False
                            record.is_admin_discount = False
                    elif record.is_office_saleform:
                        if 'Validador Transacciones Ingreso Productos de Oficina' in user:
                            record.is_admin_office = True
                            record.is_admin_primary = False
                            record.is_admin_ben_dis = False
                            record.is_admin_discount = False
                            break
                        else:
                            record.is_admin_primary = False
                            record.is_admin_office = False
                            record.is_admin_ben_dis = False
                            record.is_admin_discount = False
                    elif record.is_ben_dis_saleform:
                        if 'Validador Transacciones Ingreso Descuentos y Beneficios' in user:
                            record.is_admin_ben_dis = True
                            record.is_admin_discount = True
                            record.is_admin_primary = False
                            record.is_admin_office = False
                            break
                        else:
                            record.is_admin_primary = False
                            record.is_admin_office = False
                            record.is_admin_ben_dis = False
                            record.is_admin_discount = False
                    else:
                        record.is_admin_ben_dis = False
                        record.is_admin_primary = False
                        record.is_admin_office = False
                        record.is_admin_discount = False
            else:
                record.is_admin_primary = False
                record.is_admin_office = False
                record.is_admin_ben_dis = False
                record.is_admin_discount = False

    def action_confirm(self):
        not_pass = False
        for record in self:
            porc = 0
            for line in record.order_line:
                porc = line.d_p_id_sales
                if record.gif_real_sale != 0:
                    temp = line.price_unit * record.gif_real_sale
                else:
                    temp = line.price_unit
                # if record.gif_IepsDisplay == False and (line.gif_SaleOrderIeps != 0.00 and line.gif_SaleOrderIeps != False):
                #     porc = porc + line.gif_SaleOrderIeps
                if porc <= temp:
                    pass
                else:
                    if record.is_primary_saleform and record.is_admin_primary:
                        pass

                    elif record.is_office_saleform and record.is_admin_office:
                        pass

                    elif record.is_ben_dis_saleform and record.is_admin_ben_dis:
                        pass

                    else:
                        not_pass = True
                        
        if not_pass == True:
            record.state = 'to_approve'
        else:
            res = super(SaleOrder, self).action_confirm()
            return res

    def authorize_sales_office(self):
        for record in self:
            res = super(SaleOrder, self).action_confirm()
            return res
    
    def authorize_sales_primary(self):
        for record in self:
            res = super(SaleOrder, self).action_confirm()
            return res
    
    def authorize_sales_ben_diss(self):
        for record in self:
            res = super(SaleOrder, self).action_confirm()
            return res

    def go_back_sales(self):
        for record in self:
            record.state="draft"

    @api.onchange('gif_sale_inverse_currency','pricelist_id')
    def _gif_calculate_real_sale_sa(self):
        if self.gif_sale_inverse_currency != 0:
            self.gif_real_sale = self.gif_sale_inverse_currency
        else:
            self.gif_real_sale = 1
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_template_id = fields.Many2one('product.template')
    d_p_id_sales = fields.Integer(compute='_compute_pp_sales')
    temp_price = fields.Float(default = 0)
    gif_difference = fields.Float(string='Cantidad',default=0.0,compute='_get_diference_sale_sa')
    gif_is_different = fields.Boolean(string='Varia',default=False,compute='_get_diference_sale_sa')
    gif_use_dif = fields.Float(default = 0,compute="_onchange_price_unit_change_gif_temp_dif_sa")

    # @api.onchange('product_template_id')
    # def _onchange_product_template_id_reset_order_line_sa(self):
    #     gif_pasa = False
    #     for record in self:
    #         if record.product_template_id.name == False or record.product_template_id.detailed_type != 'product':
    #             gif_pasa = True
    #         else:
    #             gif_pasa = False
    #             if record.product_template_id.partners_details:
    #                 for p in record.product_template_id.partners_details:
    #                     if (record.order_id.partner_id.name == p.partner.name or record.order_id.partner_id.name in p.partner.name) and record.order_id.pricelist_id.currency_id.name == p.currency_sale.name:
    #                         gif_pasa = True
    #                         break
    #                     else:
    #                         gif_pasa = False
    #             else:
    #                 gif_pasa = False
    #         if gif_pasa == False:
    #             record.product_template_id = None
    #             raise exceptions.UserError(_('Este Cliente no tiene precios asignados a este producto.'))
    

    def _compute_pp_sales(self):
        for record in self:
            if record.product_template_id.porcentaje_ventas < 0 or record.product_template_id.standard_price < 0:
                raise exceptions.UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
            else:
                price = 0
                if record.product_template_id.porcentaje_ventas > 100:
                    raise exceptions.UserError(_('El descuento porcentual no puede ser mayor a 100.'))
                else:
                    if record.product_template_id.partners_details:
                        for p in record.product_template_id.partners_details:
                            if (record.order_id.partner_id.name == p.partner.name or record.order_id.partner_id.name in p.partner.name) and record.order_id.pricelist_id.currency_id.name == p.currency_sale.name:
                                price = p.partner_price
                                break
                            else:
                                price = record.product_template_id.list_price
                    else:
                        price = record.product_template_id.list_price
                    record.d_p_id_sales = ((100 - record.product_template_id.porcentaje_ventas)/100 * price)

    @api.depends('product_template_id')
    def _give_ids(self):
        for record in self:
            record.d_p = record.product_template_id.d_p_id_sales
    
    @api.onchange('product_template_id')
    def _onchange_field_uom(self):
        for record in self:
            for partner_sale in record.product_template_id.partners_details:
                if  (record.order_id.partner_id.name == partner_sale.partner.name or record.order_id.partner_id.name in partner_sale.partner.name) and record.order_id.pricelist_id.currency_id.name == partner_sale.currency_sale.name:
                    record.product_uom = partner_sale.partner_uom
                    try:
                        if record.product_uom == partner_sale.partner_uom:
                            record.product_uom = None
                    except:
                        pass

    @api.onchange('product_uom')
    def _onchange_product_uom_gsa(self):
        for record in self:
                for partner_sale in record.product_template_id.partners_details:
                    if  (record.order_id.partner_id.name == partner_sale.partner.name or record.order_id.partner_id.name in partner_sale.partner.name) and record.order_id.pricelist_id.currency_id.name == partner_sale.currency_sale.name:
                        record.product_uom = partner_sale.partner_uom

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change_sa_changer_price_something(self): 
        for record in self:
            for partner_sale in record.product_template_id.partners_details:
                if  record.order_id.partner_id.name == partner_sale.partner.name and record.order_id.pricelist_id.currency_id.name == partner_sale.currency_sale.name:
                    record.product_uom = partner_sale.partner_uom
                    record.price_unit = partner_sale.partner_price
                    record.gif_use_dif = record.price_unit

    def _onchange_price_unit_change_gif_temp_dif_sa(self):
        for record in self:
            record.gif_use_dif = 0
    

    @api.onchange('price_unit')
    def _get_diference_sale_sa(self):
        for record in self:
            record.gif_difference = 0
            record.gif_is_different = False
            if record.product_template_id.partners_details:
                for partner_sale in record.product_template_id.partners_details:
                    if record.order_id.partner_id.name == partner_sale.partner.name and record.order_id.pricelist_id.currency_id.name == partner_sale.currency_sale.name:
                        if record.price_unit != partner_sale.partner_price:
                            record.gif_is_different = True
                            record.gif_difference = record.price_unit - partner_sale.partner_price
                        else:
                            record.gif_is_different = False
                            record.gif_difference = 0