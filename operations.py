from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel

print("operations-models")

class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class BaseOperation(BaseModel):
    id: int
    date: Optional[str]
    kind: OperationKind
    amount: Decimal
    description: Optional[str]


class OperationCreate(BaseOperation):
    pass


class OperationUpdate(BaseOperation):
    pass


class Operation(BaseOperation):
    id: int

    class Config:
        from_attributes = True
