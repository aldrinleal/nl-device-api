"""
Any Pydantic models live here.
See: https://pydantic-docs.helpmanual.io/usage/models/
"""
from pydantic import BaseModel
from enum import IntEnum
from typing import List, Union
from datetime import datetime
from dyntastic import Dyntastic
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


class PowerSource(IntEnum):
    NoPowerInAnyPowerSource = 0
    SolarPower = 1
    GeneratorPower = 2
    GridPower = 3

class DeviceStatus(Dyntastic):
    __table_name__ = "device-status"
    __hash_key__ = "device_id"
    __range_key__ = "period"

    device_id: str
    period: datetime

    raw: str

    powerOn: bool

    powerSelected: PowerSource
