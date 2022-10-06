# -*- coding: utf-8 -*-
{
    'name': "Gifan - Adición de Campos en Plantilla de Producto",
    'summary': """
        Campos adicionales en ficha de producto
        """,
    'description': """
      Requerimiento que cumple:
      +RU-0077 Adición de campos en ficha de producto 
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account','Product'
    'version': '15.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account', 'sale', 'stock'],
    # 'product_expiry'
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gif_page_product.xml',
        'views/gif_packaging_view_inherit.xml',
        'views/gif_packaging_2_view_inherit.xml',
        'views/gif_hide_fields.xml',
        'views/gif_groupPriceList.xml'

        ],
    # only loaded in demonstration mode
    'demo': [],
    'License': 'LGPL-3'
}
