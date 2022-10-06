
from odoo import api, fields, models

class GifAttachmentReports(models.Model):
    _name = 'gif.attachment.reports'
    _description = 'Reporte de adjunto'

    listEstados=[
        ('draft', 'Cotización'),
        ('purchase', 'Pedido'),
        ('sale','Orden'),
        ('posted','Publicado'),
        ('cancel','Cancelado'),
        ('waiting', 'En Espera'),
        ('confirmed', 'Confirmado'),
        ('done','Hecho'),
        ('assigned', 'Listo'),
    ]

    adjSelection=[
        ('yes', 'Si'),
        ('no', 'No'),
        
    ]

    name = fields.Char(string='Nombre Referencia')
    gif_type_document = fields.Char(string='Tipo de documento')
    gif_doc_state = fields.Selection(listEstados, string='Estado del Documento')
    gif_origin_reference = fields.Char(string='Documento de Origen')
    gif_attachments = fields.Boolean(string='Adjuntos')
    gif_date_documents = fields.Datetime(string='Fecha de documento')
    user_id= fields.Char(string="Usuario")
    user_id = fields.Many2one('res.users', string='Usuario')
    gif_attachments_ids=fields.Char(string="Nombre de Documentos Adjuntos")
    gif_adj_selection = fields.Selection(adjSelection, string= "Con Adjuntos")

