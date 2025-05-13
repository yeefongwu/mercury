from pydantic import BaseModel
from typing import List

class PremiumBreakdown(BaseModel):
    name: str
    amount: float

class AlternativePremium(BaseModel):
    name: str
    coveragePremium: float
    coverageValue: str
    breakdowns: List[PremiumBreakdown]

class Premium(BaseModel):
    id: str
    coverageName: str
    coveragePremium: float
    coverageValue: str
    breakdowns: List[PremiumBreakdown]
    alternatives: List[AlternativePremium]