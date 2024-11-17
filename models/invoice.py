from odoo import models, fields, api

class Invoice(models.Model):
    """Model representing a simple invoice."""
    _name = 'simple.invoice'
    _description = 'Simple Invoice'

    name = fields.Char(
        string="Invoice Number", 
        required=True, 
        default="New"
    )
    customer_name = fields.Char(
        string="Customer Name", 
        required=True
    )
    invoice_date = fields.Date(
        string="Invoice Date", 
        default=fields.Date.context_today
    )
    due_date = fields.Date(
        string="Due Date"
    )
    total_amount = fields.Float(
        string="Total Amount", 
        compute="_compute_total_amount", 
        store=True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('paid', 'Paid'),
        ], 
        string="Status", 
        default='draft', 
        required=True
    )
    line_ids = fields.One2many(
        'simple.invoice.line', 
        'invoice_id', 
        string="Invoice Lines"
    )
    project_id = fields.Many2one(
        'project.management', 
        string="Project"
    )

    @api.model
    def create(self, vals):
        """Override the create method to generate a unique sequence for the invoice."""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('simple.invoice') or 'New'
        return super().create(vals)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        """Compute the total amount by summing up the subtotal of all invoice lines."""
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.line_ids)

    def action_send(self):
        """Mark the invoice as 'Sent' and trigger the report action."""
        self.write({'state': 'sent'})
        return self.env.ref('cresta_sales.action_invoice_report').report_action(self)

    def action_mark_paid(self):
        """Mark the invoice as 'Paid'."""
        self.write({'state': 'paid'})


class InvoiceLine(models.Model):
    """Model representing a line item in an invoice."""
    _name = 'simple.invoice.line'
    _description = 'Invoice Line'

    invoice_id = fields.Many2one(
        'simple.invoice', 
        string="Invoice", 
        required=True, 
        ondelete='cascade'
    )
    description = fields.Char(
        string="Description", 
        required=True
    )
    quantity = fields.Float(
        string="Quantity", 
        required=True, 
        default=1.0
    )
    unit_price = fields.Float(
        string="Unit Price", 
        required=True
    )
    subtotal = fields.Float(
        string="Subtotal", 
        compute="_compute_subtotal", 
        store=True
    )

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        """Compute the subtotal as the product of quantity and unit price."""
        for line in self:
            line.subtotal = line.quantity * line.unit_price
