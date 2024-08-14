from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import pyglet
from playsound import playsound


class Building(models.Model):
    _name = "building"
    _description = "Building"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'code'

    no = fields.Integer()
    code = fields.Char()
    # name = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)
