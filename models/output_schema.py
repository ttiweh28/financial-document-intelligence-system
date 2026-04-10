from pydantic import BaseModel
from typing import Optional


class ParsedDocument(BaseModel):
    raw_text: str
    page_count: Optional[int] = None
    document_type: Optional[str] = None


class FinancialEntities(BaseModel):
    vendor: Optional[str] = None
    client: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    currency: Optional[str] = None
    line_items: list[str] = []
    payment_details: Optional[str] = None


class ComputedMetrics(BaseModel):
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    tax_rate: Optional[float] = None
    total: Optional[float] = None
    is_balanced: Optional[bool] = None


class AnomalyReport(BaseModel):
    anomalies_found: bool
    anomalies: list[str] = []


class FinalReport(BaseModel):
    parsed_document: ParsedDocument
    entities: FinancialEntities
    metrics: ComputedMetrics
    anomalies: AnomalyReport
    summary: str
    explanation: str