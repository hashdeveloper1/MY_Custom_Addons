from odoo import fields, models, api


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To-Do Task'
    _order = 'id desc'
    _rec_name = 'ref'

    ref = fields.Char(compute="_compute_task_name", default='new', tracking=1)
    name = fields.Char(string="Task Name", tracking=1)
    assign_to_id = fields.Many2one('res.partner', required=True, states={'completed': [('readonly', True)], 'in_progress': [('readonly', True)]}, tracking=1)
    due_date = fields.Date(required=True, states={'completed': [('readonly', True)], 'in_progress': [('readonly', True)]}, tracking=1)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')],
        default='new', tracking=1
    )
    # description = fields.Char(states={'completed': [('readonly', True)]})
    description = fields.Text(states={'completed': [('readonly', True)]}, tracking=1)

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def _compute_task_name(self):
        for rec in self:
            rec.ref = 'Task ' + str(rec.id)
