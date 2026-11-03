from django.contrib import admin
from django.urls import path, re_path
from Safari import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_index),
    path('mostrar_login/', views.mostrar_login),
    path('login/', views.login),
    path('cerrar_sesion/', views.cerrar_sesion),
    
    path('panel_admin/', views.mostrar_panel_admin),
    path('panel_mesero/', views.mostrar_panel_mesero),
    path('panel_cajero/', views.mostrar_panel_cajero),
    
    path('administrar_productos/', views.administrar_productos),
    path('registrar_producto/', views.registrar_producto),
    path('act_pro/<int:id>/', views.form_act_producto),
    path('actualizar_producto/<int:id>/', views.actualizar_producto),
    path('eliminar_producto/<int:id>/', views.eliminar_producto),
    
    path('administrar_mesas/', views.administrar_mesas),
    path('administrar_admin_mesas/', views.administrar_admin_mesas),
    path('form_act_mes/<int:id>/', views.form_act_mes),
    path('actualizar_mesa/<int:id>/', views.actualizar_mesa),
    path('form_act_mes_adm/<int:id>/', views.form_act_mes_adm),
    path('actualizar_mesa_admin/<int:id>/', views.actualizar_mesa_admin),
    path('eliminar_mesas/<int:id>/', views.eliminar_mesas),
    path('eliminar_mesas_admin/<int:id>/', views.eliminar_mesas_admin),
    path('registrar_mesa/', views.registrar_mesa),
    path('registrar_mesa_admin/', views.registrar_mesa_admin),
    
    path('administrar_usuarios/', views.administrar_usuarios),
    path('actualizar_usuario/<int:id>/', views.actualizar_usuario),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario),
    path('registrar_usuario/', views.registrar_usuario),
    path('act_usu/<int:id>/', views.form_act_usu),
    
    path('administrar_pdv/', views.administrar_pdv),
    path('registrar_pdv/', views.registrar_pdv),
    path('act_pdv/<int:id>/', views.form_act_pdv),
    path('actualizar_pdv/<int:id>/', views.actualizar_pdv),
    path('eliminar_pdv/<int:id>/', views.eliminar_pdv),
    
    path('listado_historial/<int:orden>/', views.mostrar_listado_historial),
    path('ver_ventas/', views.ver_ventas),
    path('ver_estadisticas/', views.ver_estadisticas),
    path('exportar_excel/', views.exportar_excel),
    path('jornada/', views.jornada),
    path('ver_ventas_caja/', views.ver_ventas_caja),
    path('registrar_ventas/', views.registrar_ventas),
    path('registrar_pedido/', views.registrar_pedido),
    
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'Safari' / 'static'}),
]
