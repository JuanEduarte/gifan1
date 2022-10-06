# -*- coding: utf-8 -*-
{
    'name': "Gifan - Programación de rutas de entrega ",
    'summary': """ Generar los mecanismos necesarios para el establecimiento de Rutas de entrega de los Productos que entrega a sus Clientes """,
    'description': """ 
    Requerimientos que cumple:
     +RU-0100 - Programación de rutas de entrega 

    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'stock',
    'version': '15.0.1',
    'depends': [
        'sale','stock','account',
        ],
    'data': [
           'security/ir.model.access.csv',
           'views/gif_rutas_view.xml',
           'views/gif_filed_route_view.xml',
           'reports/gif_routes_report.xml',
           'reports/routes_report.xml',
           'data/data.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}