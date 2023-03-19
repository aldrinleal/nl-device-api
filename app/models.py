"""
Any Pydantic models live here.
See: https://pydantic-docs.helpmanual.io/usage/models/
"""
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime


class GetMetricDataRequest(BaseModel):
    StartTime: datetime
    EndTime: datetime


class MetricDataResult(BaseModel):
    Id: str
    Label: str
    Timestamps: List[datetime]
    Values: List[Union[float, int]]


class GetMetricDataResponse(BaseModel):
    MetricDataResults: List[MetricDataResult]


class HealthCheck(BaseModel):
    status: str = "ok"
