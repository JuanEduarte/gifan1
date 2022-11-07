from odoo import models, fields, api
from odoo.osv import expression
import re


class GifProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """Función sobreescrita.
            Se agrega un criterio de busqueda con base en los codigos de los proveedores del producto.
        """
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            product_ids = []
            if operator in positive_operators:
                product_ids = list(self._search([('default_code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
                if not product_ids:
                    product_ids = list(self._search([('barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
                    
                    # Se buscan los detalles de ciente que contengan el nombre, para obtener el producto al que pertenecen mediante su plantilla.
                    if not product_ids:
                        details_ids = list(self.env['gif.partners.details']._search(['|',('bar_code','=',name),('individual_code','=',name)], limit=limit, access_rights_uid=name_get_uid))
                        product_ids = [d.product_tmp_id.product_variant_id.id for d in self.env['gif.partners.details'].search([('id','in',details_ids)])]
                    
                        # Se buscan los detalles de vendedor que contengan el nombre, para obtener el producto al que pertenecen mediante su plantilla.
                        if not product_ids:
                            details_ids = list(self.env['gif.partners.details.purchase']._search(['|',('bar_code_purchase','=',name),('individual_code_purchase','=',name)], limit=limit, access_rights_uid=name_get_uid))
                            product_ids = [d.product_tmp_id_purchase.product_variant_id.id for d in self.env['gif.partners.details.purchase'].search([('id','in',details_ids)])]
                       
            if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                product_ids = list(self._search(args + [('default_code', operator, name)], limit=limit))
                if not limit or len(product_ids) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(product_ids)) if limit else False
                    product2_ids = self._search(args + [('name', operator, name), ('id', 'not in', product_ids)], limit=limit2, access_rights_uid=name_get_uid)
                    product_ids.extend(product2_ids)
            elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = expression.OR([
                    ['&', ('default_code', operator, name), ('name', operator, name)],
                    ['&', ('default_code', '=', False), ('name', operator, name)],
                ])
                domain = expression.AND([args, domain])
                product_ids = list(self._search(domain, limit=limit, access_rights_uid=name_get_uid))
            if not product_ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    product_ids = list(self._search([('default_code', '=', res.group(2))] + args, limit=limit, access_rights_uid=name_get_uid))
            # still no results, partner in context: search on supplier info as last hope to find something
            if not product_ids and self._context.get('partner_id'):
                suppliers_ids = self.env['product.supplierinfo']._search([
                    ('name', '=', self._context.get('partner_id')),
                    '|',
                    ('product_code', operator, name),
                    ('product_name', operator, name)], access_rights_uid=name_get_uid)
                if suppliers_ids:
                    product_ids = self._search([('product_tmpl_id.seller_ids', 'in', suppliers_ids)], limit=limit, access_rights_uid=name_get_uid)
        else:
            product_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        
        return product_ids