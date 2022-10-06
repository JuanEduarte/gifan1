# -*- coding: utf-8 -*-
{
    'name': "Gifan - Control de Tarimas",
    'summary': """Módulo de control de tarimas""",
    'description': """
        Requerimientos que cumple:
        +RU-0076 Control de Tarimas
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Stock',
    'version': '15.0.1',
    'depends': [
        'base',
        'stock',
        ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizards/wizard_pallet_operations_views.xml',
        'views/git_pallet_pallet_views.xml',
        'views/stock_picking_inherit_views.xml',
        # 'data/data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}