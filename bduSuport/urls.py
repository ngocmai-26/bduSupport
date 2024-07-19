from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework import permissions

from bduSuport.views.academic_level.academic_level import AcademicLevelView
from bduSuport.views.academic_level.miniapp_academic_level import MiniappAcademicLevelView
from bduSuport.views.account_management import AccountManagementView
from bduSuport.views.admin_account import AdminAccountView
from bduSuport.views.admission_registration import AdmissionRegistrationView
from bduSuport.views.college_exam_group import CollegeExamGroupView
from bduSuport.views.evaluation_method import EvaluationMethodView
from bduSuport.views.health import HealthView
from bduSuport.views.login import TokenPairView
from bduSuport.views.major.major import MajorView
from bduSuport.views.major.miniapp_major import MiniappMajorView
from bduSuport.views.news.news_menegement import NewsManagementView
from bduSuport.views.subject import SubjectView
from bduSuport.views.mini_app_auth import MiniAppAuth
from bduSuport.views.constructor import ConstructorView
from bduSuport.views.root import RootView

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

router.register('majors', MajorView, basename='major')
router.register('health', HealthView, basename='health')
router.register('news', NewsManagementView, basename='new')
router.register('subjects', SubjectView, basename='subject')
router.register('init', ConstructorView, basename='constructor')
router.register('super-admin', RootView, basename='super_admin')
router.register('miniapp/auth', MiniAppAuth, basename='account_miniapp_auth')
router.register('miniapp/majors', MiniappMajorView, basename='miniapp_majors')
router.register('academic-levels', AcademicLevelView, basename='academic_level')
router.register('evaluation-methods', EvaluationMethodView, basename='evaluation_method')
router.register('college-exam-groups', CollegeExamGroupView, basename='college_exam_group')
router.register('backoffice/accounts', AccountManagementView, basename='account_management')
router.register('backoffice/admin/accounts', AdminAccountView, basename='backoffice_admin_account')
router.register('miniapp/academic-levels', MiniappAcademicLevelView, basename='miniapp_academic-levels')
router.register('miniapp/admission-registration', AdmissionRegistrationView, basename='admission_registration')

urls = router.urls + [
   path('backoffice/login', TokenPairView.as_view(), name='backoffice_token_obtain_pair'),
]

urlpatterns = [
   path('apis/', include(urls)),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]