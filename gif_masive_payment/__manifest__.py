# -*- coding: utf-8 -*-
{
    'name': "Gif-Aplicacion y carga masiva de pagos",
    'summary': """ a plataforma impedira el registro de un pago sobre una Factura de venta siempre y cuando esta no se encuentre timbrada y con su respectivo UUID; así mismo, mediante un archivo en formato xls / xlsx se indiquen los pagos que serán aplicados a las Facturas de venta""",
    'description': """ 
     Requerimientos que cumple:
     RU-0050 - Carga masiva de Pagos

    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'account',
    'version': '15.0.1',
    'depends': [
                'base',
                'sale',
                'purchase',
                'sale', 
                'stock',
        
        ],
    'data': [
      'security/ir.model.access.csv',
      'views/gif_import_payment.xml',
      #'data/data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}