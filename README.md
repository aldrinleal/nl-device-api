# Reference

  * `yarn install && pipenv install`
  * `pipenv run sls offline`

## Format


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


## Generating timestamps:

```
[ int(time.mktime(x.timetuple())) for x in  (datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=1)) ]
[1679262355, 1679175955]

```

# Device API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A [FastAPI] [serverless] service

Generated using [cookiecutter-fastapi-template](https://github.com/miketheman/cookiecutter-fastapi-template).


## Dependencies

We have a few sets of dependencies - development, deployment, and runtime.

### Runtime Dependencies

- Python 3.8
- [FastAPI]
- Python packages installed via `pipenv install`

### Deployment Dependencies

- serverelss command line tool
- serverless plugins from `package.json`

### Development Dependencies

- Runtime Dependencies (see above)
- Python packages installed via `pipenv install --dev`

[FastAPI]: https://fastapi.tiangolo.com/
[serverless]: https://www.serverless.com/open-source/


## Structure

The main entry point to the service is `api.py`.
Start there.
