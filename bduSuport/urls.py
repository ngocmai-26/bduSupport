
from django.urls import path, include
from .views.academic_level_view import AcademicLevelViewSet
from .views.account_view import AccountViewSet
from .views.admission_registration_view import AdmissionRegistrationViewSet
from .views.evaluation_method_view import EvaluationMethodViewSet
from .views.major_view import MajorViewSet
from .views.new_view import NewViewSet
from .views.notification_view import NotificationViewSet
from .views.result_view import ResultViewSet
from .views.student_view import StudentsViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="VTicket",
      default_version='v1',
      description="VTicket",
      contact=openapi.Contact(email="ntthuan060102.work@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=()
)


router = DefaultRouter()
router.register('academic_level', AcademicLevelViewSet, basename='academic_level')
router.register('account', AccountViewSet, basename='account')
router.register('admission_registration', AdmissionRegistrationViewSet, basename='admission_registration')
router.register('evaluation_method', EvaluationMethodViewSet, basename='evaluation_method')
router.register('major', MajorViewSet, basename='major')
router.register('new', NewViewSet, basename='new')
router.register('notification', NotificationViewSet, basename='notification')
router.register('result', ResultViewSet, basename='result')
router.register('student', StudentsViewSet, basename='student')

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]