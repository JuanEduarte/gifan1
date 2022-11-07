# -*- coding: utf-8 -*-
{
    'name': "GIF - Subida de ordenes de venta",
    'summary': """Módulo de subida masiva de xslx/csv para ordenes de venta""",
    'description': """
        Desarrollo de los siguientes requerimientos:
        RU-0050 - 1 Carga masiva de Pedidos de venta (CLIENTE CHE)
        RU-0050 - 2 Carga masiva de Pedidos de venta (CLIENTE SOR) 
        RU-0050 - 3 Carga masiva de Pedidos de venta (CLIENTE HEB)
        RU-0050 - 4 Carga masiva de Pedidos de venta (CLIENTE FRSK)  
        RU-0050 - 5 Carga masiva de Pedidos de venta (CLIENTE LVP) 
        RU-0050 - 6 Carga masiva de Pedidos de venta (CLIENTE LVP REPORTE INTERNO) 
    """,

    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Stock',
    'version': '15.0.1',
    'depends': [
        'base',
        'sale',
        'gif_sale_segregation',
        'gif_purchase_segregation',
        ],

    'data': [
        'security/ir.model.access.csv',
        'views/gif_sale_order_view.xml',
        'views/gif_res_partner_view.xml',
        'wizard/wizard_sales_orders_uploader.xml',
        'wizard/wizard_default_customers.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}