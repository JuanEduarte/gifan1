from odoo import api, fields, models


class GIFPediments(models.Model):
    _name = 'gif.documents'
    _description = 'Modelo de configuración de documentos.'

    name = fields.Char(string='Nombre')
    gif_desc = fields.Char(string='Descripción')

    gif_set_data = fields.One2many(comodel_name='gif.documents.set', inverse_name='gif_doc_rel')

    @api.onchange('gif_set_data')
    def _onchange_gif_set_data(self):
        for record in self.gif_set_data:
            if record.gif_has_iva == True:
                record.gif_block_iva = False
            elif record.gif_has_iva == False:
                record.gif_block_iva = True
    #         if record.gif_dt_ref:
    #             record.gif_block_imp = True
    #             record.gif_block_com = True
    #             record.gif_block_da = True
    #             record.gif_data_type = 'R'
    #         elif record.gif_dt_imp != 0:
    #             record.gif_block_ref = True
    #             record.gif_block_com = True
    #             record.gif_block_da = True
    #             record.gif_data_type = 'I'
    #         elif record.gif_dt_com:
    #             record.gif_block_ref = True
    #             record.gif_block_imp = True
    #             record.gif_block_da = True
    #             record.gif_data_type = 'C'
    #         elif record.gif_dt_da:
    #             record.gif_block_ref = True
    #             record.gif_block_imp = True
    #             record.gif_block_com = True
    #             record.gif_data_type = 'F'
       
    

    
