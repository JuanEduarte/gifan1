# -*- coding: utf-8 -*-
{
    'name': "Gifan - Campos Adicionales",

    'summary': """
        Campos adicionales en la ficha del producto""",

    'description': """
        Requerimientos que cumple:
        + RU-0077 - Múltiples campos de información adicional de los productos 
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'stock',
        'gif_sale_segregation',
        'gif_purchase_segregation',
        
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gif_business_line_views.xml',
        'views/gif_product_category_views.xml',
        'views/gif_product_type_views.xml',
        'views/gif_product_template_inherit_views.xml',
        'views/gif_product_brand_views.xml',
        'views/gif_product_subcategory_views.xml',
        'views/gif_product_subtype_views.xml',
        'views/gif_category_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
