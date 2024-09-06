
from django.contrib import admin
from django.urls import path
from app_siad import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('download/', views.download_document, name='download_document'),
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('editais/',views.editais, name="editais"),
    path('sobre/',views.sobre, name="sobre"),
    path('adm/', views.adm, name='adm'),
    path('user/', views.user, name="user"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_representante, name='login'),
    path('cadastro/', views.registro_representante, name='cadastro')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

