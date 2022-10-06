from odoo import api, fields, models
from odoo.exceptions import UserError

class IrAttachment(models.Model):
    _inherit="ir.attachment"


    def unlink(self):
        if not self:
            return True
        self.check('unlink')

        # First delete in the database, *then* in the filesystem if the
        # database allowed it. Helps avoid errors when concurrent transactions
        # are deleting the same file, and some of the transactions are
        # rolled back by PostgreSQL (due to concurrent updates detection).

        if self.env.uid == self.create_uid.id:
            to_delete = set(attach.store_fname for attach in self if attach.store_fname)
            res = super(IrAttachment, self).unlink()
            for file_path in to_delete:
                self._file_delete(file_path)

            return res
        else: 
            raise UserError(("No puede Elminar este Documento"))

        
