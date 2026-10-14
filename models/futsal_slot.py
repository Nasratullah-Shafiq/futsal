
from odoo import models, fields


class FutsalSlot(models.Model):
    _name = 'futsal.slot'
    _description = 'Futsal Slot'

    name = fields.Char(required=True)

    weekday_id = fields.Many2one('futsal.weekday', required=True)

    start_time = fields.Char()  # "05:00 AM"
    end_time = fields.Char()    # "06:30 AM"
    