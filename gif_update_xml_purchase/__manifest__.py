# -*- coding: utf-8 -*-
{
    'name': "GIF - Subida de archivos XML y Facturas",
    'summary': """Módulo de subida masiva de XML para ordenes de compra""",
    'description': """
        Creación de módulo de xml para subida de archivos
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Stock',
    'version': '15.0.1',
    'depends': [
        'base',
        'account',
        'purchase',
        'gif_sale_segregation',
        'gif_purchase_segregation'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/gif_purchase_xml_updater_views.xml',
        'wizard/wizard_account_attachment_xml.xml',
        'wizard/wizard_account_payment_attachment.xml',
        'views/account_move_inherit_views.xml',
        'views/account_payment_inherit_views.xml',
        'wizard/wizard_xml_updater_views.xml',
        'wizard/wizard_notification_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}