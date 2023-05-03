import base64
import io
import json
import os
from datetime import datetime
from typing import Dict

import boto3

from app.models import DeviceStatus, PowerSource

STAGE = os.environ.get('STAGE', 'dev')


def init_environment():
    if 'STAGE' in os.environ.keys():
        DeviceStatus.__table_name__ = "device-status-" + os.getenv("STAGE")

    if 'AWS_REGION' in os.environ.keys():
        DeviceStatus.__table_region__ = os.getenv('AWS_REGION')


def decode_payload(device_id: str, payload_string: str) -> DeviceStatus:
    payload_bytes = base64.urlsafe_b64decode(payload_string)
    payload_bytes_stream = io.BytesIO(payload_bytes)

    """

I2C address   -> 1byte [0]	// this should be a read instruction.
  POWER ON     -> 1byte [1]   // 0x00->OFF, 0x01->ON
  POWER SELECTED  -> 1byte [2]   // 0x00->No power in any power source, 0x01->solar power, 0x02-> generator power, 0x03-> grid power
  PFC STATUS    -> 1byte [3]   // 0x00->No error with the PFC, voltage out of range. 0x01->Vbus=375-410V (+-5% of 390V)
  FUSEs STATUS   -> 1byte [4]   // 0x00->All fuses OK, 0x01->Solar fuse burnt, 0x02->Generator fuse
  BATTERY POLARITY -> 1byte [5]   // 0x00->OK polarity, 0xFF -> REVERSE POLARITY !
  TEMP STATUS   -> 1byte [6]   // 0x00->OK, 0x01->Warning High temp. 0x02->Plimit 75%Pmax, 0x03-> Plimit 50%Pmax, 0x04-> Plimit 25%Pmax, 0xFF-> OVT SHUTDOWN!
  AMBIENT TEMP   -> 2byte [7-8]  // Temp_NTC1. A reading of 2546 is 25.46C
  HTS TEMP     -> 2byte [9-10] // Temp_NTC2. A reading of 6500 is 65.00C
  Vin RMS     -> 4byte [11-14] // In mV 0-300Vrms
  Vbatt      -> 4byte [15-18] // In mV 0-60000mV
  Icharge     -> 4byte [19-22] // In mA 0-50000mA
  Battery Charge  -> 2bytes[23-24] // 0-100 is 0% to 100% charged
    """

    powerOn = (0 != int.from_bytes(payload_bytes_stream.read(1), byteorder="little"))
    powerSelected = PowerSource(
        int.from_bytes(payload_bytes_stream.read(1), byteorder="little"))

    # result["pfcStatus"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little")
    # result["fuseStatus"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little")
    # result["batteryPolarity"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little")
    # result["tempStatus"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little")
    # result["ambientTemp"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little") + (int.from_bytes(payload_bytes_stream.read(1), byteorder="little") / 100)
    # result["htsTemp"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little") + (int.from_bytes(payload_bytes_stream.read(1), byteorder="little") / 100)
    #
    # payload_bytes_stream.read(12)
    # #result["vinRms"] =  payload_bytes_stream.read(4)
    # #result["vBatt"] =  payload_bytes_stream.read(4)
    # #result["iCharge"] =  payload_bytes_stream.read(4)
    #
    # result["batteryCharge"] =  int.from_bytes(payload_bytes_stream.read(1), byteorder="little") + (int.from_bytes(payload_bytes_stream.read(1), byteorder="little") / 100)
    #
    # print(payload_bytes)

    return DeviceStatus(
        device_id=device_id,
        period=datetime.now(),
        raw=payload_string,
        powerOn=powerOn,
        powerSelected=powerSelected
    )


def handler(event: Dict[str, any], _context: any):
    init_environment()
    print("event: " + repr(event))

    # Given a Device, Decodes, Stores in DynamoDB
    device_id = event["client_id"]
    payload = event["encoded_payload"]

    device_record = decode_payload(device_id, payload)

    print("device_record: " + device_record.json())

    device_record.save()

    # If dev stage, also pushes to `u/DEVICEID`
    if 'dev' == STAGE:
        iot_data = boto3.client('iot-data')

        iot_data.publish(
            topic=f"debug/u/{device_id}",
            payload=json.dumps(event)
        )


if __name__ == '__main__':
    init_environment()
    decode_payload("PgGZQxp2BAEDAAAAAMQJxAn4lQMAUMMAAJgAAAAAADA=")
