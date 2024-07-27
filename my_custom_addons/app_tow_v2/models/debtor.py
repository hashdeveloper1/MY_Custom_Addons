from odoo import models, fields, api


class Debtor(models.Model):
    _name = "debtor"

    # name = fields.Char(string="Debtor", required=True)
    name = fields.Many2one('hr.employee', string="Debtor", required=True)
    loan_ids = fields.One2many('loan', 'debtor', readonly=1, string="Loans")
    # job_position = fields.Many2one(related="name.job_id")
    # department = fields.Many2one(related="name.department_id")
    # department = fields.Selection([
    #     ('it', 'IT'),
    #     ('system', 'System'),
    #     ('delivery', 'Delivery'),
    #     ('accounting', 'Accounting'),
    #     ('quality', 'Quality'),
    #     ('human_resources', 'Human Resources'),
    #     ('administration', 'Administration'),
    #     ('manufacturing', 'Manufacturing'),
    #     ('inventory', 'Inventory'),
    #     ('customer_services', 'Customer Services'),
    #     ('sales', 'Sales'),
    #     ('maintenance', 'Maintenance'),
    #     ('other', 'Other'),
    # ], default='other', string="Department", tracking=1)
    all_loan_values = fields.Integer(string="Loans Values", compute="_get_all_loan_values")
    all_collections = fields.Integer(string="Collected Values", compute="_get_all_collections_values")
    paid_values = fields.Integer(string="Paid Values", compute="_get_paid_values")
    exempted_values = fields.Integer(string="Exempted Values", compute="_get_exempted_values")
    all_rest_values = fields.Integer(string="Rest Values", compute="_get_all_rest_values")
    notes = fields.Char(string="Notes")
    @api.depends('loan_ids')
    def _get_all_loan_values(self):
        for rec in self:
            val = 0
            for recs in rec.loan_ids:
                val = val + recs.loan_value
            rec.all_loan_values = val

    @api.depends('loan_ids')
    def _get_all_collections_values(self):
        for rec in self:
            val = 0
            for recs in rec.loan_ids:
                val = val + recs.collections
            rec.all_collections = val

    @api.depends('loan_ids')
    def _get_paid_values(self):
        for rec in self:
            val = 0
            for recs in rec.loan_ids:
                val = val + recs.paid_value
            rec.paid_values = val

    @api.depends('loan_ids')
    def _get_exempted_values(self):
        for rec in self:
            val = 0
            for recs in rec.loan_ids:
                val = val + recs.exemption_value
            rec.exempted_values = val

    @api.depends('loan_ids')
    def _get_all_rest_values(self):
        for rec in self:
            val = 0
            for recs in rec.loan_ids:
                val = val + recs.rest_value
            rec.all_rest_values = val


# all_reste_values
# loan_number

# name = fields.Many2one('res.partner', string="Debtor", required=True)


