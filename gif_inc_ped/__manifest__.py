{
    'name': 'GIFAN -Inclusión de Pedimentos ',
    'version': '15.0.0',
    'summary': 'Definir la configuración de los documentos de importación. - GIFAN.',
    'category': '',
    'author': 'Qualsys Consulting',
    'maintainer': '',
    'website': 'http://www.qualsys.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock_landed_costs'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/gif_documents_views.xml',
        'views/gif_pediments_views.xml',
    ],
}
