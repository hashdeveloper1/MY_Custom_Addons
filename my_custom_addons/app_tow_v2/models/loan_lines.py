from odoo import models, fields, api


class LoanLines(models.Model):
    _name = "loan.lines"

    name = fields.Char(compute="_get_name")
    loan_id = fields.Many2one('loan')
    debtor = fields.Many2one(related='loan_id.debtor', string="Debtor")
    paid_date = fields.Date(required=True, string="Payment Date", default=fields.Datetime.now)
    paid_value = fields.Integer(required=True, string="Payment Value")
    rest_value = fields.Integer(string="Rest Value", compute="_compute_rest_value", store=1)
    state = fields.Selection([
        ('new', 'New'),
        ('yet', 'Yet'),
        ('done', 'Done')
    ], default='new', string="Status", tracking=1, related='loan_id.state', store=1)

    def _get_name(self):
        for rec in self:
            rec.name = "COLL/" + str('0' * (5 - len(str(rec.id)))) + str(rec.id)

    @api.depends('paid_value')
    def _compute_rest_value(self):
        for rec in self:
            rec.rest_value = rec.loan_id.loan_value - rec.loan_id.collections
            self.write({
                'rest_value': rec.rest_value,
                'paid_value': rec.paid_value,
            })

    def write(self, values):
        result = super(LoanLines, self).write(values)
        return result

