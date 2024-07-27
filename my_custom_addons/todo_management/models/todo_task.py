from odoo import fields, models, api


class TodoTask(models.Model):
    _name = 'todo.task'

    task_name = fields.Char()
    assign_to_id = fields.Many2one('res.partner')
    due_date = fields.Date()
    state = fields.Selection([
        ('', ''),
        ('', ''),
        ('', '')],
        default=''
    )
    description = fields.Text()
