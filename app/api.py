# from typing import Optional
import math

import time

from fastapi import FastAPI
# See https://fastapi.tiangolo.com/tutorial/cors/
# you can thank me later for this comment
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import HealthCheck, GetMetricDataRequest, GetMetricDataResponse, MetricDataResult

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from datetime import timedelta, datetime
from typing import Iterable


def timerange(start: datetime, end: datetime) -> Iterable[datetime]:
    start_ts, end_ts = [ int(time.mktime(x.timetuple())) for x in (start, end) ]
    upper_bound = int((end_ts - start_ts) / 60)
    if upper_bound < 0:
        upper_bound = -upper_bound
    print(f"upper_bound: {upper_bound}")
    for i in range(upper_bound):
        yield start + timedelta(minutes = i)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
def run_health_check():
    return HealthCheck()


def get_value(d: datetime) -> float:
    ts = float(d.hour * 60 + d.minute)

    return 4 * math.sin((ts / 1440.0) / (2 * math.pi))


@app.post("/metric_data")
def get_metric_data(req: GetMetricDataRequest) -> GetMetricDataResponse:
    # TODO: GetMetricDataRequest might allow other entities/fields to be read
    # TODO: Currently the API doesn't read from DynamoDB yet.
    #  Needs to be addressed once the Decoder is fully complete
    metricDataResult = MetricDataResult(
        Id="Consumption",
        Label="Consumption over Time",
        Timestamps=[],
        Values=[]
    )

    for dt in timerange(req.StartTime, req.EndTime):
        value = get_value(dt)

        metricDataResult.Timestamps.append(time.mktime(dt.timetuple()))
        metricDataResult.Values.append(value)

    return GetMetricDataResponse(
        MetricDataResults=[metricDataResult],
    )
