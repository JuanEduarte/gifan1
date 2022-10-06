
from odoo import models, fields
class GifProductTemplate(models.Model):
     _inherit="product.template"

     gif_pt_content = fields.Char(string = "Contenido Neto")
     gif_unit_contentnet= fields.Many2one('uom.uom', string = "Unidad de Contenido Neto") #lista
     gif_height = fields.Text(string="Alto")
     gif_width = fields.Text(string="Ancho")
     gif_depth = fields.Text(string="Profundidad")
     gif_weight = fields.Text(string="Peso en gramos")
     gif_active = fields.Boolean(string = "Activo")
     gif_vendCode = fields.Char(string = "Vendor Code") 
     gif_typeofbusinessline = fields.Selection(string="Tipo de Linea de Negocio",
     selection=[('other', 'Otros'),
               ('supplier', 'Proveedores')])
     gif_businessLine = fields.Many2one('res.partner', string="Linea de Negocio") 
     gif_other= fields.Text(string="Otros")
     gif_originCountry = fields.Many2many('res.country', string="País de Origen")
     gif_freecamp= fields.Text(string= "Form")
     gif_brand_ids = fields.Many2one('gif.product.brand', string='Marca')
     gif_ieps_active = fields.Boolean(string = "Producto con IEPS")
     gif_ieps_sale = fields.Many2one('account.tax', string="IEPS de Venta", domain=[('type_tax_use', '=', 'sale'),('name', 'ilike', 'IEPS')])
     gif_ieps_purchase = fields.Many2one('account.tax', string="IEPS de compra", domain=[('type_tax_use', '=', 'purchase'),('name', 'ilike', 'IEPS')])
     gif_product_type = fields.Selection(string="Tipo de Producto", 
     selection=[('PM', 'PM'), ('PT', 'PT'), ('I', 'I'), ('N', 'N')]) 
     gif_subtypeprod= fields.Selection(string="Subtipo de producto",
     selection=[('Q','Químico'),
     ('A', 'Alimento'),
     ('E', 'Etiqueta'),
     ('ME', 'Material de empaque')])
     gif_category=fields.Text(string='Categoria')
     gif_subCategory=fields.Text(string="Sub-Categoria")