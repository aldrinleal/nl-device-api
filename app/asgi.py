"""
ASGI wrapper for AWS API Gateway integration, using https://mangum.io
"""

from mangum import Mangum

from app.api import app

handler = Mangum(app)
