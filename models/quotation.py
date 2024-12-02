from odoo import models, fields, api

class Quotation(models.Model):
    _name = 'customer.quotation'
    _description = 'Customer Quotation'
    
    #Fields
    name = fields.Char(string="Quotation Reference", required=True, default="New")
    lead_id = fields.Many2one('lead.management', string="Lead", ondelete='set null')
    requirements = fields.Html(string='Requeriments')
    proposal_details = fields.Text(string="Proposal Details")
    quotation_date = fields.Date(string="Quotation Date", default=fields.Date.context_today)
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    asign_to = fields.Many2one('res.partner', string="Asign To")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('signed', 'Signed'),
        ('in_project', 'In Project'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft',  group_expand='_group_expand_states', track_visibility='always' , required=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")

    quotation_lines = fields.One2many('customer.quotation.line', 'quotation_id', string="Quotation Lines")
    
    # Group expand for status
    def _group_expand_states(self, states, domain, order):
        return [key for key, _ in self._fields['state'].selection]

    # Functions
    @api.depends('quotation_lines.subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.quotation_lines)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('customer.quotation') or 'New'
        return super(Quotation, self).create(vals)
    
    def action_send(self):
        self.write({'state': 'sent'})
        return self.env.ref('cresta_sales.action_customer_quotation_report').report_action(self)
    
    def action_mark_accepted(self):
        self.write({'state': 'accepted'})
    
    def action_send_contract(self):
        self.write({'state': 'signed'})   
        return self.env.ref('cresta_sales.action_contract_quotation_report').report_action(self) 
        
    def action_mark_rejected(self):
        self.write({'state': 'rejected'})
    
    def action_create_project(self):
        self.write({'state': 'in_project'})
        project = self.env['project.management'].create({
            'quotation_id': self.id,
            'client': self.lead_id.name,
            'project_manager': self.asign_to.id,
            'start_date': self.date_start,
            'end_date': self.date_end,
            'total_amount': self.total_amount,
            'requirements': self.requirements,
            'state': 'draft',
        })
        
        return {
            'name': 'Project',
            'view_mode': 'form',
            'res_model': 'project.management',
            'type': 'ir.actions.act_window',
            'res_id': project.id,
            'target': 'current',
        }
        
    
class QuotationLine(models.Model):
    _name = 'customer.quotation.line'
    _description = 'Quotation Line'

    # Fields
    quotation_id = fields.Many2one('customer.quotation', string="Quotation", required=True, ondelete='cascade')
    project_id = fields.Many2one('project.scope', string="Project", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Unit Price", required=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    # Functions
    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price
          
          
            
    