from odoo import models,api,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _rec_name = 'description_sale'

    def name_get(self):
        own = []
        if self._context.get('default_description_sale') != None and not self._context.get('renta_products'):
            for record in self:
                if record.description_sale != False:
                    own.append((record.id,record.name +' '+ record.description_sale))
                else:
                    own.append((record.id,record.name))
            return own
        elif self._context.get('renta_products'):
            res_names = super(ProductTemplate, self).name_get()
            result = []
            rental_product_ids = self.filtered(lambda p: p.rent_ok).ids
            for res in res_names:
                result.append((res[0], res[0] in rental_product_ids and "%s %s" % (res[1], _("(Rental)")) or res[1]))
            return result
        else:
            for record in self:
                if record.description_purchase != False:
                    own.append((record.id,record.name +' '+ record.description_purchase))
                else:
                    own.append((record.id,record.name))
            return own
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        # TDE: this could be cleaned a bit I think
        
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if d['description'] == '':
                name = '%s' % (name)
            else:
                name = '%s %s' % (name,d['description'])
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []
        company_id = self.env.context.get('company_id')

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []

        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        # Use `load=False` to not call `name_get` for the `product_tmpl_id`
        self.sudo().read(['name', 'default_code', 'product_tmpl_id'], load=False)

        product_template_ids = self.sudo().mapped('product_tmpl_id').ids
        if partner_ids:
            supplier_info = self.env['product.supplierinfo'].sudo().search([
                ('product_tmpl_id', 'in', product_template_ids),
                ('name', 'in', partner_ids),
            ])
            # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
            # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
            supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
            supplier_info_by_template = {}
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
        for product in self.sudo():
            variant = product.product_template_attribute_value_ids._get_combination_name()

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = self.env['product.supplierinfo'].sudo().browse(self.env.context.get('seller_id')) or []
            if not sellers and partner_ids:
                product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
                sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
                if not sellers:
                    sellers = [x for x in product_supplier_info if not x.product_id]
                # Filter out sellers based on the company. This is done afterwards for a better
                # code readability. At this point, only a few sellers should remain, so it should
                # not be a performance issue.
                if company_id:
                    sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    if  product.description_purchase != False:
                        mydict = {
                            'id': product.id,
                            'name': name,
                            'default_code': product.default_code,
                            'description': product.description_purchase,
                            }
                    elif product.description_sale != False:
                        mydict = {
                            'id': product.id,
                            'name': name,
                            'default_code': product.default_code,
                            'description': product.description_sale,
                            }
                    else:
                        mydict = {
                                'id': product.id,
                                'name': seller_variant or name,
                                'default_code': s.product_code or product.default_code,
                                'description': '',
                                }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                if product.description_purchase != False:
                    mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          'description': product.description_purchase,
                          }
                elif product.description_sale != False:
                    mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          'description': product.description_sale,
                          }
                else:
                    mydict = {
                            'id': product.id,
                            'name': name,
                            'default_code': product.default_code,
                            'description': '',
                            }
                result.append(_name_get(mydict))
        return result

    
        