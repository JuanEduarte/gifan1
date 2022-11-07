# -*- coding: utf-8 -*-
{
    'name': "Gifan - Ventas",

    'summary': """
        Módulo de ventas de Gifan""",

    'description': """
        Requerimientos que cumple:
        +RU-0033 Manejo de descuentos de Proveedores.
        +RU-0037 Manejo de descuentos a Clientes.
        +RU-0051 Aprobación de ventas a precios más bajos.
        +RU-0052 Precios de Clientes en productos.
        +RU-0071 Precio por tipo de Presentación (Packing) en Facturas de compra.
        +RU-0093 Verificación de Precios de compra.
        +RU-0099 Proceso de aprobación en PR y PO.
        +RU-0077 Aadición de campos en ficha de producto
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'sale',
        'purchase',
        'gif_sale_segregation',
        'gif_purchase_segregation',
        
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gif_product_template_inherit_views.xml',
        'views/gif_sale_order_inherit_views.xml',
        'views/gif_purchase_order_inherit_views.xml',
        'views/gif_partners_details.xml',
        'views/gif_account_move_inherit_views.xml',
        # 'views/gif_res_partner_inherit_views.xml',
        #------>RK
        # 'views/gif_page_product.xml',
        # 'views/gif_packaging_view_inherit.xml',
        # 'views/gif_packaging_2_view_inherit.xml',
        # 'views/gif_hide_fields.xml',
        # 'views/gif_groupPriceList.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
