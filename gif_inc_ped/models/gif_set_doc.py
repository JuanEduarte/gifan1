from odoo import api, fields, models


class GIFSetDoc(models.Model):
    _name = 'gif.documents.set'
    _description = 'Modelos para definir los campos de los documentos'

    name = fields.Char(string='Nombre')
    gif_data = fields.Char(string='Dato') #Se calculara automaticamente a función de la empresa actual
    gif_sec_des = fields.Char(string='Descripción')
    gif_con = fields.Char(string='Consecutivo')
    gif_has_iva = fields.Boolean(string='Incluye IVA')
    gif_iva = fields.Integer(string='% IVA') #Solo editable Si tiene IVA
    gif_cost = fields.Boolean(string='Acum. Costo')
    gif_debit = fields.Char(string='Cuenta Cargo')
    gif_credit = fields.Char(string='Cuenta Abono')

    gif_dt_ref = fields.Char(string='Referencia') #Tipo de Dato: Texto -> Referencia  
    gif_dt_imp = fields.Float(string='Importe') #Tipo de Dato: Decimal -> Importe
    gif_dt_com = fields.Char(string='Comentario') #Tipo de Dato: Char -> Comentario
    gif_dt_da = fields.Date(string='Fecha') #Tipo de Dato: Fecha -> Date

    gif_block_ref = fields.Boolean(default=False,compute='_onchange_gif_data_type')
    gif_block_imp = fields.Boolean(default=False,compute='_onchange_gif_data_type')
    gif_block_com = fields.Boolean(default=False,compute='_onchange_gif_data_type')
    gif_block_da = fields.Boolean(default=False,compute='_onchange_gif_data_type')

    gif_block_iva = fields.Boolean(default=True)
    gif_cal_iva = fields.Float(string='IVA Calculado', compute='_calculate_iva')
    

    gif_data_type = fields.Selection(string='Tipo de Dato', selection=[('R', 'Referencia'), ('I', 'Importe'),('C','Comentario'),('F','Fecha')])

    gif_pediment_rel = fields.Many2one(comodel_name='gif.pediments')
    gif_doc_rel = fields.Many2one(comodel_name='gif.documents')

    gif_rel_name = fields.Char('Origen')
    

    @api.onchange('gif_dt_imp')
    def _calculate_iva(self):
        for record in self:
            if record.gif_has_iva == True and record.gif_iva != 0 and record.gif_dt_imp != 0:
                record.gif_cal_iva = (record.gif_iva / 100) * record.gif_dt_imp
            else:
                record.gif_cal_iva = 0
    

    @api.onchange('gif_data_type')
    def _onchange_gif_data_type(self):
        for record in self:
            record.gif_block_ref = False
            record.gif_block_imp = False
            record.gif_block_com = False
            record.gif_block_da = False
            if record.gif_data_type == 'R':
                record.gif_block_imp = True
                record.gif_block_com = True
                record.gif_block_da = True
            elif record.gif_data_type == 'I':
                record.gif_block_ref = True
                record.gif_block_com = True
                record.gif_block_da = True
            elif record.gif_data_type == 'C':
                record.gif_block_ref = True
                record.gif_block_imp = True
                record.gif_block_da = True
            elif record.gif_data_type == 'F':
                record.gif_block_ref = True
                record.gif_block_imp = True
                record.gif_block_com = True

class GIFProdPart(models.Model):
    _name = 'gif.documents.partials'
    _description = 'Modelos para asignar las particiones'

    name = fields.Char(string='Nombre')
    gif_total_ped = fields.Float(string='Valor comercial partida')
    gif_stock_picking = fields.Many2one(comodel_name='stock.picking')
    gif_stock_product = fields.Char(string='Producto')
    gif_stock_qty = fields.Integer(string='Cantidad')
    gif_rel_ped = fields.Many2one(comodel_name='gif.pediments')
    gif_nm_part = fields.Integer(string='No. Partida')
    


    
    

    
    
    
    
    
    
    
