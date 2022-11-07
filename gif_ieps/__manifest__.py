# -*- coding: utf-8 -*-
{
    'name': "Gifan - Adición de Campo IEPS en Proveedor",
    'summary': """
        Campos adicionales en ficha de proveedor
        """,
    'description': """
      Requerimiento que cumple:
            ##+RU-0077 Adición de campos en ficha de producto 
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account','Contacts'
    'version': '15.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account', 'sale', 'contacts','purchase'],
    # 'product_expiry'
    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/gif_desgloseIEPS.xml'

        ],
    # only loaded in demonstration mode
    'demo': [],
    'License': 'LGPL-3'
}
