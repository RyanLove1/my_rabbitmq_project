from django.conf.urls import url, include
from rest_framework import routers

from MyRab import views

router = routers.DefaultRouter()

# 学生信息
router.register(r'test_rab', views.TestRabbitmq)
# 班级信息
router.register(r'my_class', views.ClassViewSet)

urlpatterns = [
    url(r'', include(router.urls)),

]
