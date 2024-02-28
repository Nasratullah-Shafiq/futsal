from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FutsalReservation(models.Model):
    _name = 'futsal.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Futsal Reservation'
    _order = 'weekday_id, slot_id'

    # -------------------------
    # BASIC INFO
    # -------------------------
    name = fields.Char(default='New', readonly=True)

    customer_id = fields.Many2one('res.partner', required=True)
    
    phone = fields.Char()

    weekday_id = fields.Many2one('futsal.weekday', required=True)

    start_time = fields.Char(
        related='slot_id.start_time',
        readonly=True,
        store=True
    )

    end_time = fields.Char(
        related='slot_id.end_time',
        readonly=True,
        store=True
    )
    
    # -------------------------
    # AVAILABLE SLOTS (CORE FIX)
    # -------------------------
    available_slot_ids = fields.Many2many(
        'futsal.slot',
        compute='_compute_available_slots',
        store=False
    )

    # -------------------------
    # SLOT (FILTERED)
    # -------------------------
    slot_id = fields.Many2one(
        'futsal.slot',
        required=True,
        domain="[('id', 'in', available_slot_ids)]"
    )

    notes = fields.Text()

    # -------------------------
    # STATE
    # -------------------------
    state = fields.Selection([
        ('booked', 'Booked'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='booked', tracking=True)

    # -------------------------
    # AUTO SEQUENCE
    # -------------------------
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('futsal.reservation')
        return super().create(vals)

    # -------------------------
    # 🔥 MAIN LOGIC (NO UI BUGS)
    # -------------------------
    @api.depends('weekday_id')
    def _compute_available_slots(self):
        for rec in self:
            if not rec.weekday_id:
                rec.available_slot_ids = False
                continue

            # booked slots for this weekday
            booked = self.env['futsal.reservation'].search([
                ('weekday_id', '=', rec.weekday_id.id),
                ('state', '=', 'booked')
            ]).mapped('slot_id')

            # all slots for weekday
            all_slots = self.env['futsal.slot'].search([
                ('weekday_id', '=', rec.weekday_id.id)
            ])

            # available = all - booked
            rec.available_slot_ids = all_slots - booked

    # -------------------------
    # VALIDATION (BACKEND SAFE)
    # -------------------------
    @api.constrains('weekday_id', 'slot_id')
    def _check_slot(self):
        for rec in self:
            if not rec.slot_id or not rec.weekday_id:
                continue

            exists = self.search_count([
                ('weekday_id', '=', rec.weekday_id.id),
                ('slot_id', '=', rec.slot_id.id),
                ('state', '=', 'booked'),
                ('id', '!=', rec.id)
            ])

            if exists:
                raise ValidationError("This slot is already booked for this day!")

    # -------------------------
    # ACTIONS
    # -------------------------
    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})