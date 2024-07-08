
from django.urls import path, include
from .views.academic_level_view import AcademicLevelView
from .views.account import AccountView
from .views.admission_registration_view import AdmissionRegistrationView
from .views.evaluation_method_view import EvaluationMethodView
from .views.major_view import MajorView
from .views.new_view import NewView
from .views.notification_view import NotificationView
from .views.result_view import ResultView
from .views.student_view import StudentsView
from .views.auth_view import AuthView
from rest_framework.routers import SimpleRouter
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


router = SimpleRouter(trailing_slash=False)
router.register('auth', AuthView, basename='auth')
router.register('academic_level', AcademicLevelView, basename='academic_level')
router.register('account', AccountView, basename='account')
router.register('admission_registration', AdmissionRegistrationView, basename='admission_registration')
router.register('evaluation_method', EvaluationMethodView, basename='evaluation_method')
router.register('major', MajorView, basename='major')
router.register('new', NewView, basename='new')
router.register('notification', NotificationView, basename='notification')
router.register('result', ResultView, basename='result')
router.register('student', StudentsView, basename='student')

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]