from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import pyglet
from playsound import playsound
import time


class Loan(models.Model):
    _name = "loan"

    name = fields.Char(compute="_get_name", readonly=1, store=1)
    debtor = fields.Many2one('debtor', required=True, string="Debtor", states={'done': [('readonly', True)], 'yet': [('readonly', True)]})
    loan_value = fields.Integer(required=True, string="Value", states={'done': [('readonly', True)], 'yet': [('readonly', True)]})
    tack_loan_date = fields.Date(required=True, default=fields.Datetime.now, string="Tacking Date", states={'done': [('readonly', True)], 'yet': [('readonly', True)]})
    payment_start_date = fields.Date(required=True, default=fields.Datetime.now, string="Payment Start date", states={'done': [('readonly', True)], 'yet': [('readonly', True)]})
    state = fields.Selection([
        ('new', 'New'),
        ('yet', 'Yet'),
        ('done', 'Done')
    ], default='new', string="Status", tracking=1, readonly=1)
    collections = fields.Integer(string="Collections Value", compute="_get_collections", store=1)
    rest_value = fields.Integer(string="Rest Value", compute="_get_rest_value", store=1)
    loan_lines_ids = fields.One2many('loan.lines', 'loan_id', string="Loan Collections")
    exemption_ids = fields.One2many('exemption', 'loan_id', string="Loan Exemptions")
    exemption_value = fields.Integer(string="Exemption Value", compute="_get_exemption_value", store=1)
    paid_value = fields.Integer(string="Paid Value", compute="_get_paid_value", store=1)
    notes = fields.Char(string="Notes")

    def _get_name(self):
        for rec in self:
            rec.name = "LO/" + str('0' * (5 - len(str(rec.id)))) + str(rec.id)

    @api.depends('loan_lines_ids', 'exemption_ids', 'loan_value', 'rest_value', 'debtor', 'state')
    def _get_collections(self):
        for rec in self:
            rec.collections = 0
            for recs in rec.loan_lines_ids:
                rec.collections = rec.collections + recs.paid_value
            for recs in rec.exemption_ids:
                rec.collections = rec.collections + recs.exemption_value

            # val = 0
            # for rec2 in rec.exemption_ids:
            #     val = val + rec2.exemption_value
            #     # rec2.rest_value = rec.loan_value - val
            #
            # for rec2 in rec.loan_lines_ids:
            #     val = val + rec2.paid_value
            #     rec2.rest_value = rec.loan_value - val

            if rec.collections > 0 and rec.state == 'new' and rec.loan_value != 0 and rec.debtor:
                rec.state = 'yet'
            self.write({
                'rest_value': rec.rest_value,
                'paid_value': rec.paid_value,
                'collections': rec.collections,
                'loan_lines_ids': rec.loan_lines_ids
            })

    @api.depends('loan_lines_ids', 'rest_value', 'loan_value', 'collections')
    def _get_rest_value(self):
        for rec in self:
            rec.rest_value = rec.loan_value - rec.collections

    @api.depends('loan_lines_ids')
    def _get_paid_value(self):
        for rec in self:
            rec.paid_value = 0
            for recs in rec.loan_lines_ids:
                rec.paid_value = rec.paid_value + recs.paid_value

    @api.depends('exemption_ids')
    def _get_exemption_value(self):
        for rec in self:
            rec.exemption_value = 0
            for recs in rec.exemption_ids:
                rec.exemption_value = rec.exemption_value + recs.exemption_value

    def action_confirm(self):
        for rec in self:
            if (rec.collections >= rec.loan_value) and (rec.loan_value != 0):
                rec.play_sound2()
                rec.state = 'done'
            elif rec.loan_value == 0:
                rec.state = 'new'

    @api.constrains('loan_value')
    def _check_loan_value_grater_zero(self):
        """ Validation Method """
        for rec in self:
            if rec.loan_value == 0:
                raise ValidationError('Please Add Loan Value!')

    @staticmethod
    def play_sound():
        playsound('/home/hashem/pythonProject/sound/sound.mp3')

    @staticmethod
    def play_sound2():
        playsound('/home/hashem/ERP/ERP_Odoo16/odoo/my_custom_addons/app_tow_v2/static/sound/confirm.mp3')

    @staticmethod
    def play_sound3():
        playsound('/home/hashem/ERP/ERP_Odoo16/odoo/my_custom_addons/app_tow_v2/static/sound/conf.wav')

    @api.model_create_multi
    def create(self, vals):
        res = super(Loan, self).create(vals)
        print("inside create method")     # This logic will do when you click on the save button
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        self.action_confirm()
        res = super(Loan, self)._search(domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None)
        print("read")
        return res

    def write(self, vals):
        res = super(Loan, self).write(vals)
        print("inside write method")
        return res

    def unlink(self):
        res = super(Loan, self).unlink()
        print("inside delete method")
        return res