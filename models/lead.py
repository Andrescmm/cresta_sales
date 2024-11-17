from odoo import models, fields, api

class Lead(models.Model):
    _name = 'lead.management'
    _description = 'Lead Management'

    # Basic fields
    name = fields.Char(string='Lead Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    description = fields.Text(string='Description')
    budget = fields.Float(string="Budget")
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    write_date = fields.Datetime(string='Last Updated', default=fields.Datetime.now)
    meeting_date = fields.Datetime(string='Meeting Date')
    requirements = fields.Html(string='Requeriments')
    

    # Related fields
    project_scope = fields.Many2one('project.scope', string='Project Scope')
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    campaign = fields.Many2one('sale.campaign', string='Campaign')
    tags = fields.Many2many('lead.tag', string='Tags')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    communication_ids = fields.One2many('lead.communication', 'lead_id', string='Communications')

    # Selection fields
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('meeting', 'Meeting'),
        ('quotation', 'Quotation'),
        ('lost', 'Lost')
    ], group_expand='_group_expand_states', default='new', string='Status')
    
    lead_source = fields.Selection([
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('campaign', 'Campaign'),
        ('other', 'Other')
    ], string="Lead Source", default='website')
    
    qualification_status = fields.Selection([
        ('cold', 'Cold'),
        ('warm', 'Warm'),
        ('lost', 'Lost'),
        ('success', 'Very Likely'),
    ], compute='_compute_qualification_status', string="Qualification Status")

    # Computed fields
    @api.depends('budget', 'campaign', 'project_scope')
    def _compute_qualification_status(self):
        for lead in self:
            if lead.budget and lead.campaign and lead.project_scope:
                lead.qualification_status = 'success'
            elif lead.budget and lead.campaign:
                lead.qualification_status = 'warm'
            elif lead.campaign:
                lead.qualification_status = 'cold'
            else:
                lead.qualification_status = 'lost'

    # Group expand for status
    def _group_expand_states(self, states, domain, order):
        return [key for key, _ in self._fields['status'].selection]

    # Override create method
    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].upper()
        return super().create(vals)

    # Actions to update status
    def action_mark_as_done(self):
        self.status = 'in_progress'
        
    def action_mark_as_lost(self):
        self.status = 'lost'


    # Action to create a quotation
    def action_make_quotation(self):
        quotation = self.env['customer.quotation'].create({
            'lead_id': self.id,
            'requirements': self.requirements,  
            'proposal_details': self.description,  
            'asign_to': self.assigned_to.id,
        })

        self.env['customer.quotation.line'].create({
            'quotation_id': quotation.id,
            'project_id': self.project_scope.id, 
            'quantity': 1,
            'unit_price': self.project_scope.price, 
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'customer.quotation',
            'view_mode': 'form',
            'res_id': quotation.id,
        }

    