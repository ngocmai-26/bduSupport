
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


router = DefaultRouter()
router.register('academic_level_view', AcademicLevelViewSet, basename='academic_level_view')
router.register('account_view', AccountViewSet, basename='account_view')
router.register('admission_registration_view', AdmissionRegistrationViewSet, basename='admission_registration_view')
router.register('evaluation_method_view', EvaluationMethodViewSet, basename='evaluation_method_view')
router.register('major_view', MajorViewSet, basename='major_view')
router.register('new_view', NewViewSet, basename='new_view')
router.register('notification_view', NotificationViewSet, basename='notification_view')
router.register('result_view', ResultViewSet, basename='result_view')
router.register('student_view', StudentsViewSet, basename='student_view')

urlpatterns = [
    path('api/', include(router.urls)),
    
]