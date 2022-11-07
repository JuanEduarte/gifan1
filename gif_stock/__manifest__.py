# -*- coding: utf-8 -*-
{
    'name': "Gifan -Cantidad Real Contable",
    'summary': """Módulo de Validación en tres fases de proceso de ingreso""",
    'description': """ 
    Requerimientos que cumple:
    +RU-0060 Validación en tres fases de proceso de ingreso

    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'stock',
    'version': '15.0.1',
    'depends': [
        'base',
        'stock',
        'sale',
        'product',
        'purchase',
        ],
    'data': [
        'views/stock_picking2_inherit_views.xml',
        'views/gif_stock_picking.xml',
        'views/gif_picking3_views.xml',
        'views/gif_purchase_units_view.xml',
        'views/gif_acount_invoice_view.xml',    
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}