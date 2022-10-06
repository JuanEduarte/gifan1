# -*- coding: utf-8 -*-
{
    'name': "Gifan - Alertas de Calidad",
    'summary': """
        Asociación de Ordenes de Compra y Venta con sus respectivas facturas en las Ordenes de Calidad
        """,
    'description': """
        Requerimientos que cumple:
      +RU-0041 Asociacion de Ordenes a calidad
      
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account','Product'
    'version': '15.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account', 'sale'],
    # always loaded
    'data': [
        'views/gif_quality_alert_views_inherit.xml',
        
        ],
    # only loaded in demonstration mode
    'demo': [],
    'License': 'LGPL-3'
}