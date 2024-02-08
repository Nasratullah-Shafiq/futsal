from odoo import models, fields


class FutsalWeekday(models.Model):
    _name = 'futsal.weekday'
    _description = 'Futsal Weekday'

    name = fields.Char(required=True)

    slot_ids = fields.One2many('futsal.slot', 'weekday_id')
    