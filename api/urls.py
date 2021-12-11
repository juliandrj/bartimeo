from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'menu', views.MenuViewSet)
router.register(r'plantas', views.PlantaViewSet)
router.register(r'estadosPlanta', views.EstadoPlantaObservacionViewSet)
router.register(r'tareas', views.TareaViewSet)

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^', include(router.urls)),
    url(r'^auth/', obtain_jwt_token),
    url(r'^verify/', verify_jwt_token)
]