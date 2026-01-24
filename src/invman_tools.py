from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import Field, BaseModel

from src.invman_client.api.business_partners_api import BusinessPartnersApi
from src.invman_client.api.files_api import FilesApi
from src.invman_client.api.invoice_positions_api import InvoicePositionsApi
from src.invman_client.api.invoice_templates_api import InvoiceTemplatesApi
from src.invman_client.api.invoices_api import InvoicesApi
from src.invman_client.api.sales_taxes_api import SalesTaxesApi
from src.invman_client.api_client import ApiClient
from src.invman_client.configuration import Configuration
from server import mcp

config = Configuration(
    host = "http://localhost:8080/invoice-manager-server"
)
api_client = ApiClient(configuration=config)
business_partner_api = BusinessPartnersApi(api_client=api_client)
files_Api = FilesApi(api_client=api_client)
invoice_positions_api = InvoicePositionsApi(api_client=api_client)
invoice_template_api = InvoiceTemplatesApi(api_client=api_client)
invoices_api = InvoicesApi(api_client=api_client)
sales_taxes_api = SalesTaxesApi(api_client=api_client)

@mcp.tool()
async def get_all_invoices(paid: Annotated[Optional[bool], Field(description="Filter invoices by paid status")] = None, customer_number: Annotated[Optional[int], Field(description="Filter invoices by customer number")] = None, receiver_id: Annotated[Optional[int], Field(description="Filter invoices by receiver")] = None, order_number: Annotated[Optional[str], Field(description="Filter invoices by order number")] = None):
    """Get a list of all invoices with optional filters for paid status, customer number, receiver id, and order number."""
    invoices = invoices_api.get_all_invoices(paid=paid, customer_number=customer_number, receiver_id=receiver_id, order_number=order_number)
    return invoices


class Invoice(BaseModel):
    id: int  | None
    description: str | None
    viaMail: bool | None
    preText: str | None
    postText: str | None
    serviceFrom: datetime
    serviceTo: datetime | None
    orderNumber: str | None
    customerNumber: int
    paid: bool | None
    positions: list[int] | None
    receiver: int | None
    salexTax: int
    invocieTemplate: int
    file: int | None


@mcp.tool()
async def create_invoice(invoice: Invoice):
    """Create a new invoice based on the provided invoice data."""
    created_invoice = await invoices_api.create_invoice(invoice)
    return created_invoice

@mcp.tool()
async def get_all_sales_taxes():
    """Get a list of all sales taxes."""
    sales_taxes = await sales_taxes_api.get_all_sales_taxes()
    return sales_taxes

@mcp.tool()
async def get_all_business_partners(name: Annotated[Optional[str], Field(description="Filter business partners by name")] = None):
    """Get a list of all business partners with optional filter by name."""
    business_partners = await business_partner_api.get_all_business_partners(name=name)
    return business_partners

@mcp.tool()
async def get_all_invoice_templates():
    """Get a list of all invoice templates."""
    invoice_templates = await invoice_template_api.get_all_invoice_templates()
    return invoice_templates


class Unit(Enum):
    HOUR = "hour"
    PD= "pd"
    PIECE = "piece"


class InvoicePosition(BaseModel):
    id: int | None
    description: str | None
    pricePerUnitIncents: int
    quantity: float
    unit: Unit
    invoice: int


@mcp.tool()
async def create_position(position: InvoicePosition):
    """Create a new invoice position based on the provided Invoice Position object."""
    created_position = await invoice_positions_api.create_position(position)
    return created_position

@mcp.tool()
async def update_invoice_by_id(id: Annotated[int, Field(description="The id of the invoice")], invoice: Invoice):
    """Update the details of an existing invoice using its unique identifier."""
    updated_invoice = await invoices_api.update_invoice_by_id(id=id, invoice=invoice)
    return updated_invoice

@mcp.tool()
async def get_invoice_pdf_by_id(id: Annotated[int, Field(description="The id of the invoice")]):
    """Generate a pdf file for the invoice with the given id and returns its unique identifier."""
    pdf = await invoices_api.get_invoice_pdf_by_id(id=id)
    return pdf

@mcp.tool()
async def download_file_by_id(id: Annotated[int, Field(description="The id of the file")]):
    """Download a file by its unique identifier."""
    file = await files_Api.download_file_by_id(id=id)
    return file


