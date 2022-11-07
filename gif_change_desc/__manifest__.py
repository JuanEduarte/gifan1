# -*- coding: utf-8 -*-
{
    'name': "Gifan - Cambiar descripciones.",

    'summary': """
        Cambiar la descripción en ordenes.""",

    'description': """
        Cambia la descripción del producto a: Referencia interna + Nombre del product + Descripción
    """,

    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '15.0.1',
    'external_dependencies': {
        'python': [],
    },

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'purchase',
    ],

    # always loaded
    'data': [
        'views/gif_product_product_inherit_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
