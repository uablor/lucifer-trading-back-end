# settings.py
from rest_framework.response import Response
from rest_framework import status

globals().update({
    "Response": Response,
    "status": status,
})
