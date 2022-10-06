from odoo import models,fields,api


class GifQualityPoint(models.Model):
    _inherit = 'quality.point'

    gif_product_brand = fields.Many2many(comodel_name='gif.product.brand', string='Marca') 

    def _get_checks_values(self, products, company_id, existing_checks=False):
        quality_points_list = []
        point_values = []
        if not existing_checks:
            existing_checks = []
        for check in existing_checks:
            point_key = (check.point_id.id, check.team_id.id, check.product_id.id)
            quality_points_list.append(point_key)

        for point in self:
            if not point.check_execute_now():
                continue
            point_products = point.product_ids

            if point.product_category_ids:
                point_product_from_categories = self.env['product.product'].search([('categ_id', 'child_of', point.product_category_ids.ids), ('id', 'in', products.ids)])
                point_products |= point_product_from_categories

            if point.gif_product_brand:
                print('Ids: ',point.gif_product_brand.ids)
                print('Name: ',products.name)
                print('Brand id: ',products.gif_brand_ids.id)
                point_product_from_brands = self.env['product.product'].search(([('gif_brand_ids','in',point.gif_product_brand.ids),('id', 'in', products.ids)]))
                point_products |= point_product_from_brands 

            if not point.product_ids and not point.product_category_ids and not point.gif_product_brand:
                point_products |= products

            for product in point_products:
                if product not in products:
                    continue
                point_key = (point.id, point.team_id.id, product.id)
                if point_key in quality_points_list:
                    continue
                point_values.append({
                    'point_id': point.id,
                    'team_id': point.team_id.id,
                    'product_id': product.id,
                })
                quality_points_list.append(point_key)

        return point_values


class GifBrand(models.Model):
    _inherit = 'gif.product.brand'

    gif_rel_point = fields.Many2one(comodel_name='quality.point')
    

