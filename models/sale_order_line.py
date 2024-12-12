from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    note_general = fields.Boolean(string="General Note")

    @api.model
    def create(self, vals):
        context = self.env.context
        if context.get('default_note_general'):
            vals['note_general'] = True
        return super(SaleOrderLine, self).create(vals)

    @api.model
    def write(self, vals):
        context = self.env.context
        if context.get('default_note_general'):
            vals['note_general'] = True
        return super(SaleOrderLine, self).write(vals)