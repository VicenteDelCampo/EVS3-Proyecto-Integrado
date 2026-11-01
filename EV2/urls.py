from django.contrib import admin
from django.urls import path
from Safari import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_index),
    path('mostrar_login/', views.mostrar_login),
    path('login/', views.login),
    path('panel_admin/', views.mostrar_panel_admin),
    path('panel_mesero/', views.mostrar_panel_mesero),
    path('panel_cajero/', views.mostrar_panel_cajero),
    path('administrar_mesas/', views.administrar_mesas),
    path('administrar_admin_mesas/', views.administrar_admin_mesas),
    path('registrar_mesa/', views.registrar_mesa),
    path('registrar_mesa_admin/', views.registrar_mesa_admin),
    path('administrar_usuarios/', views.administrar_usuarios),
    path('administrar_pdv/', views.administrar_pdv),
    path('ver_ventas/', views.ver_ventas),
    path('ver_estadisticas/', views.ver_estadisticas),
    path('jornada/', views.jornada),
    path('ver_ventas_caja/', views.ver_ventas_caja),
    path('registrar_ventas/', views.registrar_ventas),
    path('registrar_pedido/', views.registrar_pedido),
    path('registrar_usuario/', views.registrar_usuario),
    path('act_usu/<int:id>/', views.form_act_usu),
    path('actualizar_usuario/<int:id>/', views.actualizar_usuario),


]
