from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.feedback import Feedback
from bduSuport.validations.create_feedback import CreateFeedbackValidator

class FeedbackView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
        
    @swagger_auto_schema(request_body=CreateFeedbackValidator)
    def create(self, request):
        try:
            validate = CreateFeedbackValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            feedback = Feedback(**validate.validated_data, creator=request.user)
            feedback.save()

            if feedback.id == None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo ý kiến!").response

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"FeedbackView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response