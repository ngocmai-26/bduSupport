from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework import permissions

from bduSuport.views.mini_app_auth import MiniAppAuth
from bduSuport.views.new_view import NewView
from bduSuport.views.health import HealthView
from bduSuport.views.login import TokenPairView
from bduSuport.views.anonymous_account import AnonymousAccountView
from bduSuport.views.major_view import MajorView
from bduSuport.views.result_view import ResultView
from bduSuport.views.student_view import StudentsView
from bduSuport.views.notification_view import NotificationView
from bduSuport.views.academic_level_view import AcademicLevelView
from bduSuport.views.evaluation_method_view import EvaluationMethodView
from bduSuport.views.admission_registration_view import AdmissionRegistrationView

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


router = SimpleRouter(trailing_slash=False)
router.register('new', NewView, basename='new')
router.register('major', MajorView, basename='major')
router.register('health', HealthView, basename='health')
router.register('result', ResultView, basename='result')
router.register('student', StudentsView, basename='student')
router.register('backoffice/account', AnonymousAccountView, basename='backoffice_account')
router.register('notification', NotificationView, basename='notification')
router.register('academic-level', AcademicLevelView, basename='academic_level')
router.register('miniapp/auth', MiniAppAuth, basename='account_miniapp_auth')
router.register('evaluation-method', EvaluationMethodView, basename='evaluation_method')
router.register('admission-registration', AdmissionRegistrationView, basename='admission_registration')

urls = router.urls + [
   path('backoffice/login', TokenPairView.as_view(), name='backoffice_token_obtain_pair'),
]

urlpatterns = [
   path('apis/', include(urls)),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]