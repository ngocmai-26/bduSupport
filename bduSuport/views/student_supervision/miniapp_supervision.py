import logging
from dataclasses import asdict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.student_supervision_registration import StudentSupervisionRegistration
from bduSuport.services.bdu_dw.bdu_dw import BduDwService
from bduSuport.validations.date_filter import DateFilter
from bduSuport.validations.date_range_filter import DateRangeFilter

class MiniappStudentSupervisionView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @action(methods=["GET"], detail=True, url_path="attendances")
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("from_date", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("to_date", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ]) 
    def get_attendances(self, request, pk):
        try:
            logging.getLogger().info("MiniappStudentSupervisionView.get_attendances pk=%s, params=%s", pk, request.query_params)

            validate = DateRangeFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Bạn chỉ có thể xem dữ liệu trong 30 ngày liên tiếp!").response

            if not StudentSupervisionRegistration.objects.filter(deleted_at=None, miniapp_user=request.user, student_dw_code=pk).exists():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Bạn không có quyền xem dữ liệu sinh viên này!").response
            
            attendances = BduDwService().get_attendances_by_student_code_and_date_range(
                student_code=pk,
                date_start=validate.validated_data["from_date"],
                date_end=validate.validated_data["to_date"]
            )
            result = [asdict(attendance) for attendance in attendances]
            sorted_result = sorted(result, key=lambda x: x["attendance_date"], reverse=True)

            return RestResponse(sorted_result).response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionView.get_attendances exc=%s, pk=%s, params=%s", e, pk, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="scores")
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("semester", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter("academic_year", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
    ]) 
    def get_scores(self, request, pk):
        try:
            logging.getLogger().info("MiniappStudentSupervisionView.get_scores pk=%s, params=%s", pk, request.query_params)

            if not StudentSupervisionRegistration.objects.filter(deleted_at=None, miniapp_user=request.user, student_dw_code=pk).exists():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Bạn không có quyền xem dữ liệu sinh viên này!").response
            
            scores = BduDwService().get_student_scores(
                student_code=pk,
                semester=request.query_params.get("semester", 1),
                academic_year=int(request.query_params.get("academic_year", 0))
            )
            result = [asdict(score) for score in scores]

            return RestResponse(result).response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionView.get_scores exc=%s, pk=%s, params=%s", e, pk, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="time-tables")
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("date", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ]) 
    def get_time_tables(self, request, pk):
        try:
            logging.getLogger().info("MiniappStudentSupervisionView.get_time_tables pk=%s, params=%s", pk, request.query_params)

            validate = DateFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Bạn chỉ có thể xem dữ liệu trong 30 ngày liên tiếp!").response

            if not StudentSupervisionRegistration.objects.filter(deleted_at=None, miniapp_user=request.user, student_dw_code=pk).exists():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Bạn không có quyền xem dữ liệu sinh viên này!").response
            
            time_tables = BduDwService().get_time_tables(
                student_code=pk,
                date=validate.validated_data["date"],
            )
            result = [asdict(time_table) for time_table in time_tables]
            sorted_result = sorted(result, key=lambda x: x["start_period"], reverse=False)

            return RestResponse(sorted_result).response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionView.get_time_tables exc=%s, pk=%s, params=%s", e, pk, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    @action(methods=["GET"], detail=True, url_path="events")
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("start_year", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter("semester", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
    ])
    def get_events(self, request, pk):
        try:
            logging.getLogger().info("MiniappStudentSupervisionView.get_events pk=%s, params=%s", pk, request.query_params)

            start_year = request.query_params.get("start_year")
            semester = request.query_params.get("semester")
            if start_year is None or semester is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Missing start_year or semester").response
            try:
                start_year = int(start_year)
                semester = int(semester)
            except ValueError:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="start_year and semester must be integers").response

            nkhk = int(f"{start_year % 100}{(start_year + 1) % 100}{semester}")

            if not StudentSupervisionRegistration.objects.filter(deleted_at=None, miniapp_user=request.user, student_dw_code=pk).exists():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Bạn không có quyền xem dữ liệu sinh viên này!").response

            events = BduDwService().get_student_events(
                student_code=pk,
                nkhk=nkhk
            )
            result = [asdict(event) for event in events]
            return RestResponse(result).response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionView.get_events exc=%s, pk=%s, params=%s", e, pk, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response