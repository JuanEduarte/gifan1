from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    descount_selector = fields.Selection(string='Tipo de Descuento', selection=
    [('1', 'Precio Fijo'), 
    ('2', 'Precio Porcentual'),],default='1',required=True)
    d_p = fields.Integer('Descuento Porcentual para compras', default=0, required=True)
    d_f = fields.Float('Descuento Fijo para compras', default=0.0, required=True)
    porcentaje_ventas = fields.Integer('Porcentaje de venta', default=0, required=True)
    partners_details = fields.One2many('gif.partners.details', 'product_tmp_id')
    partners_details_purchase = fields.One2many('gif.partners.details.purchase', 'product_tmp_id_purchase')
    #--------> RK
    gif_pt_content = fields.Char(string = "Contenido Neto")
    gif_unit_contentnet= fields.Many2one('uom.uom', string = "Unidad de Contenido Neto") #lista
    gif_height = fields.Char(string="Alto")
    gif_width = fields.Char(string="Ancho")
    gif_depth = fields.Char(string="Profundidad")
    gif_weight = fields.Char(string="Peso en gramos")
    gif_active = fields.Boolean(string = "Activo")
    gif_vendCode = fields.Char(string = "Vendor Code") 
    gif_typeofbusinessline = fields.Many2one('producttemplate.product_template', string="Tipo de Linea de Negocio",
    selection=[('other', 'Otros'),
    ('supplier', 'Proveedores')])
    gif_businessLine = fields.Many2one('res.partner', string="Linea de Negocio") 
    gif_other= fields.Char(string="Otros")
    gif_originCountry = fields.Many2many('res.country', string="País de Origen")
    gif_freecamp= fields.Text(string= "Form")
    gif_brand_ids = fields.Many2one('gif.product.brand', string='Marca')
    gif_ieps_active = fields.Boolean(string = "Producto con IEPS")
    gif_ieps_sale = fields.Many2one('account.tax', string="IEPS de Venta", domain=[('type_tax_use', '=', 'sale'),('name', 'ilike', 'IEPS')])
    gif_ieps_purchase = fields.Many2one('account.tax', string="IEPS de compra", domain=[('type_tax_use', '=', 'purchase'),('name', 'ilike', 'IEPS')])
    gif_product_type = fields.Selection(string="Tipo de Producto GIFAN", 
    selection=[('PM', 'PM'), 
    ('PT', 'PT'), 
    ('I', 'I'), 
    ('N', 'N')]) 
    gif_subtypeprod= fields.Selection(string="Subtipo de producto",
    selection=[('Q','Químico'),
    ('A', 'Alimento'),
    ('E', 'Etiqueta'),
    ('ME', 'Material de empaque')])
    gif_category=fields.Char(string='Categoria')
    gif_subCategory=fields.Char(string="Sub-Categoria")
    #--------> RK

    @api.onchange('descount_selector')
    def _onchange_descount_selector(self):
        for record in self:
            record.d_f = 0
            record.d_p = 0
            
    

    @api.onchange('partners_details.partner_price')
    def validate(self):
        for record in self:
            for line in record.order_line:
                if self.standard_price >= line.partners_details.partner_price:
                    raise UserError(_('No se puede tener precios negativos. Por favor revisa tu producto'))
                else:
                    pass
