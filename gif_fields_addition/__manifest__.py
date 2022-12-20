{
    'name': "Gifan - Adición de campos en recepciones y entegas.",
    'version': '15.0.1',
    'depends': ['base',
        'stock',
        'delivery',
        'sale',
        'purchase',
        'gif_sale_segregation',
        'gif_purchase_segregation'],
        
    'author': "Qualsys Consulting",

    'sumary' : "Adición de fecha de caducidad en recepciones y entregas."
    ,
    'category': 'customization',
    
    'description': """
        Requerimientos que cumple:
        +RU-0044 - Adición de campos en recepciones
        +RU-0045 - Adición de campos en entregas 
    """,
    
    'data': [
        "views/gif_stock_move_line_views.xml",
        "views/gif_stock_quant_view.xml",
    ],
    
    
    'license': 'LGPL-3',
}
