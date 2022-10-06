{
    'name': "Gifan - Asignación de Empleados",
    'version': '15.0.1',
    'depends': ['base','mrp'],
    'author': "Qualsys Consulting",
    'sumary' : "Asignación de Empleados",
    'category': 'customization',
    'description': """
        Requerimientos que cumple:
        +RU-0105 Asignación de actividades
    """,
    
    # data files always loaded at installation
    'data': [
        "security/ir.model.access.csv",
        "views/gif_disponibilidad_views.xml",
        'views/gif_history_views.xml',
        "views/mrp_production_views.xml",
                
    ],
    
    
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    
    'license': 'LGPL-3',
}
