# -*- coding: utf-8 -*-
{
    "name": "Cotización Technystand",
    "version": "16.0.1.0.0",
    "sequence": -1,
    "category": "Accounting",
    "summary": "Plantilla de cotización personalizada para TechnyStand",
    "description": """
        Este módulo proporciona una plantilla de cotización personalizada.
    """,
    "author": "Luis Miguel GJ",
    "maintainer": "LuisCodes",
    "license": "AGPL-3",
    "depends": ["base", "sale"],
    "data": [
        "views/sale_order_views.xml",
        "reports/invoice_report.xml",
        "reports/reports.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
}
