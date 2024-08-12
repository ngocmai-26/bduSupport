from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework import permissions

from bduSuport.views.academic_level.academic_level import AcademicLevelView
from bduSuport.views.academic_level.miniapp_academic_level import MiniappAcademicLevelView
from bduSuport.views.account_management import AccountManagementView
from bduSuport.views.admin_account import AdminAccountView
from bduSuport.views.admission_registration.admission_registration import AdmissionRegistrationView
from bduSuport.views.admission_registration.admission_registration_management import AdmissionRegistrationManagementView
from bduSuport.views.business_recruiment.business_recruiment import BusinessRecruimentView
from bduSuport.views.business_recruiment.business_recruiment_management import BusinessRecruimentManagementView
from bduSuport.views.college_exam_group.college_exam_group_management import CollegeExamGroupView
from bduSuport.views.custom_refresh_token_view import CustomRefreshTokenView
from bduSuport.views.evaluation_method import EvaluationMethodView
from bduSuport.views.feedback.feedback import FeedbackView
from bduSuport.views.feedback.feedback_management import FeedbackManagementView
from bduSuport.views.health import HealthView
from bduSuport.views.login import TokenPairView
from bduSuport.views.major.major import MajorView
from bduSuport.views.major.miniapp_major import MiniappMajorView
from bduSuport.views.news.miniapp_news import MiniappNewsView
from bduSuport.views.news.news_menegement import NewsManagementView
from bduSuport.views.news.news_type_management import NewsTypeManagementView
from bduSuport.views.root.backoffice_account_management import BackofficeAccountManagementView
from bduSuport.views.subject.subject_management import SubjectView
from bduSuport.views.mini_app_auth import MiniAppAuth
from bduSuport.views.constructor import ConstructorView
from bduSuport.views.root.root import RootView

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

health_router = SimpleRouter(trailing_slash=False)
miniap_router = SimpleRouter(trailing_slash=False)
backoffice_router = SimpleRouter(trailing_slash=False)

health_router.register('health', HealthView, basename='health')

miniap_router.register('init', ConstructorView, basename='constructor')
miniap_router.register('news', MiniappNewsView, basename='miniapp_news')
miniap_router.register('auth', MiniAppAuth, basename='account_miniapp_auth')
miniap_router.register('majors', MiniappMajorView, basename='miniapp_majors')
miniap_router.register('feedbacks', FeedbackView, basename='miniapp_feedback')
miniap_router.register('business-recruiments', BusinessRecruimentView, basename='business_recruiments')
miniap_router.register('academic-levels', MiniappAcademicLevelView, basename='miniapp_academic_levels')
miniap_router.register('admission-registration', AdmissionRegistrationView, basename='admission_registration')

backoffice_router.register('super-admin', RootView, basename='super_admin')
backoffice_router.register('majors', MajorView, basename='major_management')
backoffice_router.register('subjects', SubjectView, basename='subject_management')
backoffice_router.register('news', NewsManagementView, basename='news_management')
backoffice_router.register('accounts', AccountManagementView, basename='account_management')
backoffice_router.register('feedbacks', FeedbackManagementView, basename='feedback_management')
backoffice_router.register('news-types', NewsTypeManagementView, basename='news_type_management')
backoffice_router.register('admin/accounts', AdminAccountView, basename='backoffice_admin_account')
backoffice_router.register('academic-levels', AcademicLevelView, basename='academic_level_management')
backoffice_router.register('evaluation-methods', EvaluationMethodView, basename='evaluation_method_management')
backoffice_router.register('college-exam-groups', CollegeExamGroupView, basename='college_exam_group_management')
backoffice_router.register('business-recruiments', BusinessRecruimentManagementView, basename='business_recruiments_management')
backoffice_router.register('admission-registration', AdmissionRegistrationManagementView, basename='admission_registration_management')
backoffice_router.register('super-admin/accounts/backoffice', BackofficeAccountManagementView, basename='backoffice_account_management')

backoffice_urls = backoffice_router.urls + [
   path('login', TokenPairView.as_view(), name='backoffice_token_obtain_pair'),
   path('refresh', CustomRefreshTokenView.as_view(), name='backoffice_token_refresh_token'),
]

urlpatterns = [
   path('apis/', include(health_router.urls)),
   path('apis/backoffice/', include(backoffice_urls)),
   path('apis/miniapp/', include(miniap_router.urls)),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]