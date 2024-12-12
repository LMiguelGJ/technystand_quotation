from odoo import models, fields, api
from collections import defaultdict  
from odoo.exceptions import UserError 
import locale


class Order(models.Model):
    _inherit = "sale.order"
    _description = "Order"

    forma_pago = fields.Char(
        string="Forma de Pago",
        default="Pago por cheque o transferencia bancaria por el (100%) del valor total de la cotización para entregar la mercancía.",
    )

    origen_materiales = fields.Char(string="Origen de los Materiales", default="ESPAÑA")

    garantia_comercial = fields.Char(
        string="Garantía Comercial",
        default="1 año contra defectos de fabricación. Validez de la oferta: 15 Días.",
    )
    tiempo_entrega = fields.Char(
        string="Tiempo de Entrega",
        default="INMEDIATO a partir de la fecha de colocación de la orden de compra, después de haber recibido el pago del 100%.",
    )

    bank_account_info = fields.Char(string="Cuenta Bancaria")
    
    pickup_location = fields.Char(
        string="Lugar de Retiro",
        default="",
        # default="EL CLIENTE RETIRA LA MERCANCIA ARMADA EN NUESTRO ALMACEN EN MANOGUYABO.",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(Order, self).default_get(fields_list)
        self._onchange_bank_account_info()
        self.action_calculate_section_totals()
        return res

    @api.onchange("pricelist_id")
    def _onchange_bank_account_info(self):
        for order in self:
            if order.pricelist_id.currency_id.name == "DOP":
                order.bank_account_info = "Banco BHD LEON - Cuenta Corriente en pesos #11596860016 - Tramerías y Soluciones de Almacenaje T.S.A. S.R.L"
            elif order.pricelist_id.currency_id.name == "USD":
                order.bank_account_info = "Banco BHD - Cuenta de ahorro en dolares #11596860041 - Tramerías y Soluciones de Almacenaje T.S.A. S.R.L"
            else:
                order.bank_account_info = "No hay información disponible para esta moneda."

    section_totals = fields.Text(string="Section Totals", readonly=True)

    def action_calculate_section_totals(self):
        for order in self:
            section_totals = defaultdict(float)
            current_section = None

            # Agrupación de subtotales por sección
            for line in order.order_line:
                if line.display_type:  # Si es una sección
                    current_section = line.name
                elif current_section and line.display_type is False:  # Si es una línea regular
                    section_totals[current_section] += line.price_subtotal
                    
            # Crear el mensaje en formato de texto
            message = ""
            for section, total in section_totals.items():
                formatted_total = locale.format_string("%.2f", total, grouping=True)
                message += f"{section}: {formatted_total}\n"

            order.section_totals = message

    @api.onchange("order_line")
    def _onchange_order_line(self):
        self.action_calculate_section_totals()
        
    @api.onchange("order_line")
    def _onchange_order_line(self):
        self.action_calculate_section_totals()
        for line in self.order_line:
            if line.display_type == 'line_note_general':  # {{ edit_1 }}
                line.name = line._get_sale_order_line_multiline_description_sale()  # Hereda el comportamiento de line_note
