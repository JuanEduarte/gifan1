{
  'name': 'Gif-Carta porte',
  'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'stock',
    'version': '15.0.1',
    'depends': [
        'sale','stock','account','gif_sale_segregation','gif_purchase_segregation','l10n_mx_edi_stock','l10n_mx_edi_stock_extended_40'],
    'data': [
           'views/gif_consigment_note_button.xml',
           'views/gif_load_note.xml',
           'views/consignment_inh_views.xml',
           'security/ir.model.access.csv',
            ],
  'qweb': [
  ],
  'sequence': 1,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': '- Arkademy Part 1',
  'summary': 'Catat Penjualan Sederhana',
  'license': 'OPL-1',
  'description': '-'
}