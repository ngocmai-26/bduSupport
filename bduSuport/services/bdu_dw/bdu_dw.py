import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import logging
from dataclasses import asdict

from bduSuport.helpers.http import is_2xx
from bduSuport.services.bdu_dw.dto import BduStudentDto
from bduSuport.services.bdu_dw.key_mapper import convert_list
from bduSuport.services.bdu_dw.mapping_dicts import student_key_mapping
from bduSuport.models.bdu_student import BduStudent

class BduDwService:
    __base_url = ""
    __username = ""
    __password = ""

    def __init__(self):
        self.__base_url = config("BDU_DATA_WAREHOUSE_GATEWAY_BASE_URL")
        self.__username = config("BDU_DATA_WAREHOUSE_GATEWAY_USERNAME")
        self.__password = config("BDU_DATA_WAREHOUSE_GATEWAY_PASSWORD")        

    def get_attendances(self):
        pass

    def get_students(self) -> list[BduStudentDto]:
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