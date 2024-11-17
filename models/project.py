from odoo import models, fields, api

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'

    # Fields
    name = fields.Char(string="Project Name", required=True, default="New")
    quotation_id = fields.Many2one('customer.quotation', string="Quotation")
    invoice_id = fields.Many2one('simple.invoice', string="Invoice")
    project_manager = fields.Many2one('res.users', string="Project Manager", default=lambda self: self.env.user)
    client = fields.Char(string="Client")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    total_amount = fields.Float(string="Invoice Total", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string="Status", default='draft', group_expand='_group_expand_states', track_visibility='always', required=True)
    task_ids = fields.One2many('project.task', 'project_id', string="Tasks")
    
    # Group expand for status
    def _group_expand_states(self, states, domain, order):
        return [key for key, _ in self._fields['state'].selection]

   # Functions
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('project.management') or 'New'
        return super(Project, self).create(vals)
    
    def action_start_project(self):
        self.write({'state': 'in_progress'})

    def action_complete_project(self):
        self.write({'state': 'completed'})    
        
    def action_make_payment(self):
        self.write({'state': 'in_progress'})
        invoice = self.env['simple.invoice'].create({
            'customer_name': self.client,
            'due_date': self.end_date,
            'total_amount': self.total_amount,
            'state': 'draft',
            'project_id': self.id,
        })
        self.env['simple.invoice.line'].create({
            'invoice_id': invoice.id,
            'description': "Project Payment",
            'quantity': 1,
            'unit_price': self.total_amount,
        })
        self.invoice_id = invoice.id
        
        return {
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'simple.invoice',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        
        
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
