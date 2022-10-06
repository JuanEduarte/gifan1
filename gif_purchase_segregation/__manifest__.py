# -*- coding: utf-8 -*-
{
    'name': "Gifan - Segregación de flujo de compras",

    'summary': """
         Clasificar y Segregar flujos de negocio en compras - Gifan""",

    'description': """
        Requerimientos que cumple:
        +RU-0014 Clasificación y segregación de Facturas de compra.
        +RU-0016 Clasificación y segregación de Notas de crédito de Facturas de compra.
        +RU-0087 Clasificación y segregación de Pedidos de compra.
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'hr',
        'purchase',
        'purchase_requisition',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gif_account_move_inherit_views.xml',
        'views/gif_account_payment_inherit_views.xml',
        'views/gif_account_batch_payment_inherit_views.xml',
        'views/gif_hr_employee_inherit_views.xml',
        'views/gif_purchase_order_inherit_views.xml',
        'views/gif_product_template_inherit_views.xml',
        'views/gif_purchase_requisition_inherit_views.xml',
        'views/gif_payment_register_inherit_views.xml',
        'data/data_purchase.xml',
    ],
    'assets':{
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
