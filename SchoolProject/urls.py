"""
URL configuration for SchoolProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Admin import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.login, name='login'),
                  path('login/', views.login, name='login'),
                  path('home/', views.home, name='home'),
                  path('register/', views.register, name='register'),
                  path('student_panel/', views.student_panel, name='student_panel'),
                  # path('fee_panel', views.fee_panel, name='fee_panel'),
                  path('add_student/', views.add_student, name='add_student'),
                  path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
                  path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
                  path('logout/', views.logout_view, name='logout'),
                  # path('fee_payments/<int:student_id>/', views.Fee_payments, name='fee_payments'),
                  path('student_fee_status/', views.student_fee_status_view, name='student_fee_status'),
                  path('add_edit_fee_detail/', views.add_edit_fee_detail_view, name='add_fee_detail'),
                  path('add_edit_fee_detail/<int:fee_status_id>/', views.add_edit_fee_detail_view, name='edit_fee_detail')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
