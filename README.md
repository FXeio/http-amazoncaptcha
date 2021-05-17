# http-amazoncaptcha

A simple http server wrapper to solve amazon's captcha using [amazoncaptcha](https://pypi.org/project/amazoncaptcha/)

## Installation

If you'd like to, activate a virtualenv

```bash
python3 -m venv venv
./venv/bin/activate
```

Then install requirements

```bash
python -m pip install -r requirements.txt
```

## How to use

### Resolve with image url

Send a GET request to /resolve with query params `?url=<imageUrl>`

### Resolve with image file

Send a POST request to /resolve with the captcha image as raw body

### Response schema

Every response (both success or failure) is a json with at least a `meta` field

Success response example:

```json
{
  "meta": {
    "code": 200,
    "message": "Success"
  },
  "data": {
    "captcha": "PBYJNT"
  }
}
```

Failure response example:

```json
{
  "meta": {
    "code": 415,
    "message": "Unsupported Media Type: Provided image is invalid"
  }
}
```

`code` field in `meta` reflects the HTTP status code

## Why?

I need a way to resolve Amazon's captchas from a node.js application
