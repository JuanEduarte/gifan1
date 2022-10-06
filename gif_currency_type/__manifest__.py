# -*- coding: utf-8 -*-
{
    'name': "Gifan - Tipo de Moneda",
    'summary': """
        Muestra el tipo de moneda en los documentos de Ingresos y Egresos.
        """,
    'description': """
        Requerimientos que cumple:
        +RU-0023 Visualizacion de La Moneda utilizada en documentos de Ingreso
        +RU-0024 Visualizacion de La Moneda utilizada en documentos de Egreso
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account','Product'
    'version': '15.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account', 'sale', 'purchase', 'stock'],
    # 'product_expiry'
    # always loaded
    'data': [

        'views/gif_sale_report_inherit.xml',
        'views/gif_account_payment_client.xml',
        'views/gif_account_report_payment_receipt_prov_view.xml',
        'views/gif_account_report_payment_receipt_view.xml',
        'views/gif_invoice_report_inherit.xml',
        'views/gif_print_batch_payment_views_inherit.xml',
        'views/gif_purchase_report_inherit.xml',

        ],
    # only loaded in demonstration mode
    'demo': [],
    'License': 'LGPL-3'
}