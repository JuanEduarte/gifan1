# -*- coding: utf-8 -*-
{
    'name': "Gifan - Adendas",
    'summary': """Módulo para configurar las adendas.""",
    'description': """
        Desarrollo de los siguientes requerimientos:
        + RU-0065 - Configuración de adendas
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Stock',
    'version': '15.0.1',
    'depends': [
        'base',
        'account',
        # 'account_edi_40',
        'l10n_mx',
        'base_vat',
        'gif_firm_desactivation',
        # 'gif_account_edi_providers'
        # 'gif_ieps',
        ],
    'data':[
        'data/addendas/addenda_amazon.xml',
        'data/addendas/addenda_bedbath.xml',
        'data/addendas/addenda_chedraui.xml',
        'data/addendas/addenda_cityfresko.xml',
        'data/addendas/addenda_costco.xml',
        'data/addendas/addenda_heb.xml',
        'data/addendas/addenda_liverpool.xml',
        'data/addendas/addenda_nadro.xml',
        'data/addendas/addenda_panadero.xml',
        'data/addendas/addenda_soriana.xml',
        'data/addendas/addenda_walmart.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}