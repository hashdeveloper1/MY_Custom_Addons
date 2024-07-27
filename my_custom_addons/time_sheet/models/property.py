from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date
import calendar

class Property2(models.Model):
    _name = "property2"
    _description = 'Property2'
    # name = fields.Char(required=True, default='New', size=30)
    total_worked_hours = fields.Float(string='Work Hours', compute='_compute_Total_worked_hours', store=True)
    name = fields.Many2one(
        'res.partner', string='Employee',
        required=True
    )

    number_month = fields.Integer(required=True, string="Working Month")
    date_availability = fields.Date()
    pro_line_ids = fields.One2many(
        'pro.lines',
        'emp_id'
    )
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    @api.depends('pro_line_ids')
    def _compute_Total_worked_hours(self):
        for recs in self:
            recs.total_worked_hours = 0
            for rec in recs.pro_line_ids:
                recs.total_worked_hours = recs.total_worked_hours + rec.worked_hours



class ProLines(models.Model):
    _name = "pro.lines"
    _description = 'Pro lines'

    date = fields.Date(default=fields.Datetime.now, required=True)
    is_attend = fields.Boolean(default=True, string="Is Attend")
    day_name = fields.Char(string="Day", compute="_get_day_name")
    time_in = fields.Datetime(string="Time In", default=fields.Datetime.now)
    time_out = fields.Datetime()
    shift_hours = fields.Integer(string="Work Hours", compute="_get_shift_hours")
    worked_hours = fields.Float(string='Work Hours', compute='_compute_worked_hours', store=True, readonly=True)
    emp_id = fields.Many2one(
        'property2'
    )

    _sql_constraints = [
        ('unique_date', 'unique("date")', 'This name is exist!')
    ]

    @api.model
    def create(self, values):
        line = super(ProLines, self).create(values)
        return line

    def write(self, values):
        result = super(ProLines, self).write(values)
        return result

    def _get_shift_hours(self):
        for rec in self:
            if rec.emp_id:
                if rec.emp_id.number_month < 7:
                    rec.shift_hours = 10
                else:
                    rec.shift_hours = 9

    @api.depends('time_in', 'time_out')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                delta = attendance.time_out - attendance.time_in
                attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = False

    @api.depends('date')
    def _get_day_name(self):
        for rec in self:
            rec.day_name = calendar.day_name[rec.date.weekday()]


