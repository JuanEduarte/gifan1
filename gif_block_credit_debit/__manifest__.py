# -*- coding: utf-8 -*-
{
    'name': "Gifan - Bloqueo de Precio de venta e impuestos",

    'summary': """
        Bloquear precio de venta e impuestos en notas de credito y debito""",

    'description': """
        En las respectivas notas de credito y debito se bloquea el poder modificar el precio de venta
        y los impuestos.
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'account'
    ],

    # always loaded
    'data': [
        #'wizard/wizard_show_groups_views.xml',
        #'security/ir.model.access.csv',
        #'security/security.xml',
        'views/gif_account_move_inherit_views.xml',
        #'views/gif_res_partner_inherit_views.xml',
        #'views/gif_sale_order_inherit_views.xml',
        #'views/gif_purchase_order_inherit_views.xml',
        #'views/gif_product_template_inherit_views.xml',
    ],
    #'assets':{
     #   'web.assets_backend':[
      #      'gif_different_social_reasons/static/src/js/gif_hide_button.js'
       # ]
    #},
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
