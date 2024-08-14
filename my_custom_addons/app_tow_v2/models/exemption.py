from odoo import models, fields, api


class Exemption(models.Model):
    _name = "exemption"

    name = fields.Char(compute="_get_name")
    loan_id = fields.Many2one('loan')
    debtor = fields.Many2one(related='loan_id.debtor', string="Debtor")
    exemption_date = fields.Date(required=True, string="Exemption Date", default=fields.Datetime.now)
    exemption_value = fields.Integer(required=True, string="Exemption Value")
    rest_value = fields.Integer(string="Rest Value", readonly=1, compute="_get_rest_value")
    notes = fields.Char(string="Notes", size=30)
    state = fields.Selection([
        ('new', 'New'),
        ('yet', 'Yet'),
        ('done', 'Done')
    ], default='new', string="Status", tracking=1, related='loan_id.state', store=True)

    def _get_name(self):
        for rec in self:
            rec.name = "Exemption/" + str(rec.id).zfill(5)
            # rec.name = "Exemption/" + str('0' * (5 - len(str(rec.id)))) + str(rec.id)

    @api.depends('loan_id')
    def _get_rest_value(self):
        for rec in self:
            rec.rest_value = rec.loan_id.rest_value
