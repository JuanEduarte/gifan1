# -*- coding: utf-8 -*-
{
    'name': "Gifan - Segregación de flujos de negocio ventas",

    'summary': """
         Clasificar y Segregar flujos de negocio en ventas - Gifan""",

    'description': """
        Requerimientos que cumple:
        +RU-0015 Clasificación y segregación de Facturas de venta.
        +RU-0017 Clasificación y segregación de Notas de crédito de Facturas de venta.
        +RU-0049 Clasificación y segregación de Pedidos de venta.
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'hr',
        'sale',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gif_account_move_inherit_views.xml',
        'views/gif_account_payment_inherit_views.xml',
        'views/gif_account_batch_payment_inherit_views.xml',
        'views/gif_hr_employee_inherit_views.xml',
        'views/gif_sale_order_inherit_views.xml',
        'views/gif_product_template_inherit_views.xml',
        'views/gif_payment_register_inherit_views.xml',
        'data/data_sale.xml',
    ],
    'assets':{
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
