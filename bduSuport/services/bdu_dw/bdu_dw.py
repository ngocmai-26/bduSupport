import logging
import requests
from datetime import date
from decouple import config
from requests.auth import HTTPBasicAuth

from bduSuport.helpers.http import is_2xx
from bduSuport.services.bdu_dw.dto import Attendance, BduStudentDto
from bduSuport.services.bdu_dw.key_mapper import convert_keys, convert_list
from bduSuport.services.bdu_dw.mapping_dicts import student_key_mapping, attendance_key_mapping

class BduDwService:
    __base_url = ""
    __username = ""
    __password = ""

    def __init__(self):
        self.__base_url = config("BDU_DATA_WAREHOUSE_GATEWAY_BASE_URL")
        self.__username = config("BDU_DATA_WAREHOUSE_GATEWAY_USERNAME")
        self.__password = config("BDU_DATA_WAREHOUSE_GATEWAY_PASSWORD")

    def get_attendances_by_student_code_and_date_range(self, student_code: int, date_start: date, date_end: date):
        try:
            resp = requests.get(
                f"{self.__base_url}/dim_danh_sach_diem_danh_odp",
                params={
                    "mssv": student_code,
                    "ngay_origin_start": date_start.strftime("%Y-%m-%d"),
                    "ngay_origin_end": date_end.strftime("%Y-%m-%d"),
                },
                auth=HTTPBasicAuth(self.__username, self.__password),
                verify=False
            )

            if not is_2xx(resp.status_code):
                logging.getLogger().error("BduDwService.get_attendances_by_student_code_and_date_range status_code not is 2xx student_code=%s, content=%s", student_code, resp.text)
                return []
            
            dataset = resp.json()

            if not isinstance(dataset, list):
                logging.getLogger().error("BduDwService.get_attendances_by_student_code_and_date_range response is not a list student_code=%s, content=%s", student_code, resp.text)
                return []
            
            if len(dataset) == 0:
                logging.getLogger().info("BduDwService.get_attendances_by_student_code_and_date_range response is empty student_code=%s, content=%s", student_code, resp.text)
                return []
            
            converted_dataset = convert_list(dataset, attendance_key_mapping)
            attendances = [Attendance(**converted_data) for converted_data in converted_dataset]
            
            return attendances
        except Exception as e:
            logging.getLogger().exception("BduDwService.get_attendances_by_student_code_and_date_range exc=%s, resp_content=%s", str(e), resp.text)
            return []

    def get_students(self):
        try:
            resp = requests.get(
                f"{self.__base_url}/fact_ho_so_sinh_vien_odp",
                auth=HTTPBasicAuth(self.__username, self.__password),
                verify=False
            )

            if not is_2xx(resp.status_code):
                logging.getLogger().error("BduDwService.get_students status_code not is 2xx content=%s", resp.text)
                return []
            
            dataset = resp.json()
            converted_dataset = convert_list(dataset, student_key_mapping)
            students = [BduStudentDto(**converted_data) for converted_data in converted_dataset]
            
            return students
        except Exception as e:
            logging.getLogger().exception("BduDwService.get_students exc=%s, resp_content=%s", str(e), resp.text)
            return []
    
    def get_student(self, student_id: str):
        try:
            resp = requests.get(
                f"{self.__base_url}/fact_ho_so_sinh_vien_odp",
                params={
                    "mssv": student_id
                },
                auth=HTTPBasicAuth(self.__username, self.__password),
                verify=False
            )

            if not is_2xx(resp.status_code):
                logging.getLogger().error("BduDwService.get_student status_code not is 2xx student_id=%s, content=%s", student_id, resp.text)
                return None
            
            data = resp.json()

            if not isinstance(data, list):
                logging.getLogger().error("BduDwService.get_student response is not a list student_id=%s, content=%s", student_id, resp.text)
                return None
            
            if len(data) == 0:
                logging.getLogger().error("BduDwService.get_student response is empty student_id=%s, content=%s", student_id, resp.text)
                return None
            
            student = convert_keys(data[0], student_key_mapping)
            student_dto = BduStudentDto(**student)
            
            return student_dto
        except Exception as e:
            logging.getLogger().exception("BduDwService.get_student exc=%s, student_id=%s, resp_content=%s", str(e), student_id, resp.text)
            return None