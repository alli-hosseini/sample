from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from schedule.application import commands
from shared.adapter.decorators import exception_handler, serialize
from shared.application.bus import bus, query_bus
from shared.domain import ValueException
from shared.application.interfaces import NoQueryResultException
from schedule.application.queries import ScheduleQuery
from . import serializers


@api_view(["POST"])
@exception_handler(exceptions=[ValueException, NoQueryResultException])
@serialize(serializers.CreateScheduleSerializer)
def create_schedule(request: Request):

    command = commands.CreateSchedule(
        vendor_id=request.data["vendor_id"],
        unit=request.data["unit"],
        value=request.data["value"],
        categories=request.data["categories"],
    )

    bus.handle(command)
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@exception_handler(exceptions=[NoQueryResultException])
def get_schedule(request: Request, vendor_id: str):
    query = ScheduleQuery(vendor_id=vendor_id)
    result = query_bus.ask(query)
    return Response(data=result, status=status.HTTP_200_OK)
