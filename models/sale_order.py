from odoo import models, fields, api


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

    @api.model
    def default_get(self, fields_list):
        res = super(Order, self).default_get(fields_list)
        self._onchange_bank_account_info()
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
