from odoo import models, fields, api, exceptions, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gif_business_rel = fields.Many2one(comodel_name='gif.business.line', string='Líneas de negocio',domain=[('gif_active_line','=',True)])
    gif_active = fields.Boolean(string = "Activo")
    gif_category_rel = fields.Many2one(comodel_name='gif.product.category', string='Categoria del producto',domain=[('gif_category_active','=',True)])
    gif_type_rel = fields.Many2one(comodel_name='gif.product.type', string='Tipo de producto GIFAN',domain=[('gif_type_active','=',True)])
    gif_subcategory_rel = fields.Many2one(comodel_name='gif.product.subcategory', string='Subcategoria',domain=[('gif_subcategory_active','=',True)])
    gif_form = fields.Char(string='Form')
    gif_brand_ids = fields.Many2one('gif.product.brand', string='Marca')
    gif_has_ieps = fields.Boolean(string='Con IEPS')
    gif_subtype_rel = fields.Many2one(comodel_name='gif.product.subtype', string='Subtipo del producto')
    gif_cate_rel = fields.Many2one(comodel_name='gif.category', string='Categoria')
    gif_ieps_sale_por = fields.Integer(string='Valor Porcentual IEPS')
    gif_ieps_sale_fij = fields.Integer(string='Valor Fijo IEPS')
    gif_ieps_purchase_por = fields.Integer(string='Valor Porcentual IEPS')
    gif_ieps_purchase_fij = fields.Integer(string='Valor Fijo IEPS')
    gif_hazard_active = fields.Boolean(string='Material Peligroso')
    gif_unit_content= fields.Many2one('uom.uom', string = "Unidad de Contenido Neto")
    gif_height = fields.Float(string="Alto")
    gif_width = fields.Float(string="Ancho")
    gif_depth = fields.Float(string="Profundidad")
    gif_weight = fields.Float(string="Peso en gramos")
    gif_originCountry = fields.Many2one('res.country', string="País de Origen")
    gif_countryCode = fields.Char(related='gif_originCountry.code',string='Código del País')
    gif_bed_number = fields.Integer(string='Empaques por cama')
    gif_bed_pallet = fields.Integer(string='Camas por tarima')
    gif_package_pallet = fields.Integer(string='Empaque secundario por Tarima')
    gif_pieces_pallet = fields.Integer(string='Piezas totales por tarima')
    
    
    
    
    
    
    
    
    

    
    
    
    
    