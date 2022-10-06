# -*- coding: utf-8 -*-
{
    'name': "Gifan - Reporte de archivos adjuntos",
    'summary': "Módulo de reportes de archivos adjuntos y bloque al eliminar",
    'description': """
        Requerimientos que cumple:
        +RU-0039 Reporte De Seguimiento De Documentación Adjunta
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Customization',
    'version': '15.0.1',
    'depends': [
        'base',
        'account',
        'sale',
        'purchase'
        ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_attachment_report_views.xml',
        'views/gif_attachment_reports.xml',

    ],
    
    # 'assets':{
    #     'web.assets_backend':[
    #         '/gif_attachments_reports/static/src/js/attachment_delete_confirm_dialog.js'
    #     ]
    # },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}