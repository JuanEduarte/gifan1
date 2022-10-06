{
    'name': "Gifan - Cantidades Mayores",
    'version': '15.0.1',
    'depends': ['base','stock'],
    'author': "Qualsys Consulting",
    'sumary' : "Modelo de Cantidades mayores en Compras",
    'category': 'customization',
    'description': """
        Requerimientos que cumple:
        +RU-0095 Deshabilitar la opción de recepción adicional de productos
        +RU-0102 Cantidades mayores
    """,
    
    # data files always loaded at installation
    'data': [
        "views/gif_stock_move_line_views.xml",
        "views/gif_stock_picking_views.xml",
                
    ],
    
    
    # data files containing optionally loaded demonstration data
    'demo': [
        #'demo/demo_data.xml',
    ],
    # 'assets':{
    #     'web.assets_backend':[
    #         'gif_larger_amounts/static/src/js/gif_hide_button.js'
    #     ]
    # },
    
    'license': 'LGPL-3',
}
