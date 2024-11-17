from odoo import models, fields, api

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'

    name = fields.Char(string="Project Name", required=True, default="New")
    # invoice_id = fields.Many2one('account.move', string="Invoice", domain=[('move_type', '=', 'out_invoice')])
    project_manager = fields.Many2one('res.users', string="Project Manager", default=lambda self: self.env.user)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    total_amount = fields.Float(string="Invoice Total", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string="Status", default='draft', required=True)
    task_ids = fields.One2many('project.task', 'project_id', string="Tasks")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('project.management') or 'New'
        return super(Project, self).create(vals)

    def action_start_project(self):
        self.write({'state': 'in_progress'})

    def action_complete_project(self):
        self.write({'state': 'completed'})


class Task(models.Model):
    _name = 'project.task'
    _description = 'Task'

    name = fields.Char(string="Task Name", required=True)
    project_id = fields.Many2one('project.management', string="Project", required=True, ondelete='cascade')
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    deadline = fields.Date(string="Deadline")
    description = fields.Text(string="Description")
    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string="Status", default='todo')

    def action_start_task(self):
        self.write({'state': 'in_progress'})

    def action_complete_task(self):
        self.write({'state': 'done'})
