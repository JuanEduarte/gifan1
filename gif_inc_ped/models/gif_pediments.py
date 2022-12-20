from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


CUSTOM_NUMBERS_PATTERN = re.compile(r'[0-9]{2}  [0-9]{2}  [0-9]{4}  [0-9]{7}')

#Crear estado de abierto y cerrado, al estar cerrado no pueden modificar nada. Listo
#Siempre que no hayan prorrateado el pedimento pueden volver de cerrado a abierto. Pend
#Al prorratear que ese pedimento ya no pueda volver a ser abierto (esconder botón). Pend
#Solo un pedimento por orden de recepción. Pend
#Solo pueden escoger el pedimento en el costo destino si está cerrado, si lo tratan de poner y sigue abierto sale una ventana de error.
#Nuevo notebook donde al escoger una orden de recepción se trae los productos y sus cantidades (solo ordenes hechas) y poderle ligar una partida de ese mismo pedimento.
#Validación que el producto tiene que tener una partida valida del mismo documento.



class GIFPediments(models.Model):
    _name = 'gif.pediments'
    _description = 'Captura de Pedimentos'

    name = fields.Char(string='No. Pedimento')
    state = fields.Selection(string='Estado', selection=[('draft', 'Abierto'), ('done', 'Cerrado'),],default='draft')
    
    gif_doc_ref = fields.Many2many(comodel_name='gif.documents',string='Documento de pedimento')
    gif_date = fields.Date(string='Fecha Pedimento')
    gif_dol_val = fields.Float(string='Valor dolares')
    gif_dol_inv = fields.Float(string='Tipo de cambio',digits=(12,4))
    gif_flete = fields.Float(string='Flete')
    gif_inc = fields.Float(string='Otros Incrementos')
    gif_ad_val = fields.Float(string='Valor Aduana',compute='_gif_calculate_ad_val')
    gif_igi = fields.Float(string='Total IGI')
    gif_dta = fields.Float(string='Total DTA')
    gif_ieps = fields.Float(string='Total IEPS')

    gif_aduana = fields.Char(string='Aduana')
    gif_change = fields.Many2one(comodel_name='res.currency', string='Moneda')
    gif_seg = fields.Float(string='Seguros')
    gif_emb = fields.Float(string='Embalajes')
    gif_com_val = fields.Float(string='Valor Comercial',compute="_get_com_val")
    gif_contract = fields.Float(string='Contra Prestac')
    gif_pre_val = fields.Float(string='Prevalidación')
    gif_iva = fields.Float(string='Total IVA')
    gif_pallets = fields.Float(string='Pallets')

    gif_total = fields.Float(string='Gasto Calculado',compute='_onchange_gif_set_ped')
    
    gif_set_ped = fields.One2many(comodel_name='gif.documents.set',inverse_name='gif_pediment_rel')
    gif_set_part = fields.One2many(comodel_name='gif.partials', inverse_name='gif_rel_pedi')

    gif_prorrateado = fields.Boolean(default=False)
    gif_ped_stock = fields.Many2one(comodel_name='stock.picking', string='Orden de entrega',domain=[('picking_type_code','=','incoming'),('state','=','done'),('gif_has_pediment','=',False)])
    gif_rel_doc_ped = fields.One2many(comodel_name='gif.documents.partials', inverse_name='gif_rel_ped')

    gif_part_part_one = fields.One2many(comodel_name='gif.set.partials', inverse_name='gif_rel_part_part')
    
    
    @api.onchange('gif_part_part_one')
    def _onchange_gif_part_part_one(self):
        for record in self.gif_part_part_one:
            if record.gif_part_prod.gif_porc_igi != False and record.gif_part_prod.gif_porc_igi != 0:
                record.gif_part_porc = record.gif_part_prod.gif_porc_igi
    
    @api.constrains('gif_rel_doc_ped')
    def _check_gif_rel_doc_ped(self):
        pedi = []
        rel_pedi = []
        for record in self.gif_rel_doc_ped:
            rel_pedi.append(record.gif_nm_part)
        for line in self.gif_part_part_one:
            pedi.append(line.gif_part_num_set)
        for r in rel_pedi:
            if r not in pedi and r != 0:
                raise ValidationError(_('Hay una partida no registrada.'))

    @api.onchange('gif_ped_stock')
    def _onchange_gif_ped_stock(self):
        purchase = self.env['purchase.order'].search([('name','=',self.gif_ped_stock.origin)])
        no_part = {}
        for record in self.gif_ped_stock.move_ids_without_package:
            for p in purchase.order_line:
                if record.product_id.name == p.product_template_id.name:
                    price = p.price_subtotal
                    break
            self.env['gif.documents.partials'].create([{
                'gif_rel_ped': self.id,
                'gif_total_ped': price,
                'gif_stock_product': record.product_id.name,
                'gif_stock_qty': record.quantity_done,
            }])
    
    def set_done(self):
        self.state = 'done'

    def go_back(self):
        self.state = 'draft'
    

    def _gif_pediments_check_no_pediment(self):
        self.ensure_one()
        if self.name:
            return [num.strip() for num in self.name.split(',')]
        else:
            return []

    @api.constrains('name')
    def _gif_validate_no_pediment(self):
        custom_numbers = self._gif_pediments_check_no_pediment()
        if any(not CUSTOM_NUMBERS_PATTERN.match(custom_number) for custom_number in custom_numbers):
            raise ValidationError(_(
                """El numero de pedimento debe de tener el siguiente formato:
                - 2 dígitos del año de validación seguidos de 2 espacios.
                - 2 dígitos del despacho de aduana seguidos de dos espacios.
                - 4 dígitos del número de serie seguidos de dos espacios.
                - 1 dígito correspondiente a la última cifra del año en curso, salvo en el caso de una aduana consolidada 
                    iniciada en el año anterior a la solicitud original de rectificación.
                - 6 dígitos de la numeración progresiva de la aduana.
                Por ejemplo: 15  48  3009  0001234""",
            ))
        else:
            exist = self.env['gif.pediments'].search([('name','=',self.name)])
            if len(exist) > 1:
                raise ValidationError(_('Ya existe ese Numero de Pedimento'))
            else:
                pass
    

    @api.onchange('gif_set_ped','gif_seg','gif_emb','gif_flete','gif_inc','gif_contract','gif_pre_val')
    def _onchange_gif_set_ped(self):
        seg_no_iva = self.gif_seg #/ 1.16
        emb_no_iva = self.gif_emb #/ 1.16
        flete_no_iva = self.gif_flete #/ 1.16
        inc_no_iva = self.gif_inc #/ 1.16
        con_no_iva= self.gif_contract #/ 1.16
        pre_no_iva = self.gif_pre_val #/ 1.16
        self.gif_total = 0
        self.gif_total = self.gif_total+ seg_no_iva + emb_no_iva + flete_no_iva + inc_no_iva + con_no_iva + pre_no_iva
        for record in self.gif_set_ped:
            if record.gif_data_type == 'I' and record.gif_cost == True:
                self.gif_total = self.gif_total + record.gif_dt_imp
                 #
            else:
                pass
    

    @api.onchange('gif_dol_val','gif_dol_inv')
    def _get_com_val(self):
        for record in self:
            record.gif_com_val = 0
            if record.gif_dol_inv != 0 and record.gif_dol_val != 0:
                record.gif_com_val = record.gif_dol_inv * record.gif_dol_val
            else:
                record.gif_com_val = 0

    @api.onchange('gif_dol_val','gif_dol_inv','gif_flete','gif_seg','gif_emb')
    def _gif_calculate_ad_val(self):
        for record in self:
            seg_no_iva = record.gif_seg #/ 1.16
            emb_no_iva = record.gif_emb #/ 1.16
            flete_no_iva = record.gif_flete #/ 1.16
            inc_no_iva = record.gif_inc #/ 1.16
            record.gif_ad_val = record.gif_com_val + flete_no_iva + seg_no_iva + emb_no_iva + inc_no_iva

    @api.onchange('gif_doc_ref')
    def _onchange_gif_doc_ref(self):
        try:
            for record in self.gif_doc_ref[-1].gif_set_data:
                ac_name = record.gif_doc_rel.name
                data = record.gif_data
                search = self.env['gif.documents.set'].search([('gif_pediment_rel','=',self.id),('gif_rel_name','=',ac_name)])
                if search and search.gif_data == data:
                    pass
                else:
                    ped = self.env['gif.documents.set'].create([{
                        'gif_data': data,
                        'gif_sec_des':record.gif_sec_des,
                        'gif_con': record.gif_con,
                        'gif_pediment_rel': self._origin.id or self.id,
                        'gif_cost': record.gif_cost,
                        'gif_iva': record.gif_iva,
                        'gif_rel_name': ac_name,
                        'gif_data_type': record.gif_data_type,
                        'gif_has_iva': record.gif_has_iva,
                    }])
        except:
            pass

    @api.onchange('gif_set_part')
    def _onchange_gif_set_part(self):
        for record in self.gif_set_part:
            for igi in self.gif_part_part_one:
                if record.gif_part_no != False and record.gif_part_no != 0 and record.gif_no_igi != 0 and record.gif_no_igi != False:
                    if record.gif_part_no == igi.gif_part_num_set:
                        record.gif_imp_igi = record.gif_no_igi * (igi.gif_part_porc / 100)
                        break

