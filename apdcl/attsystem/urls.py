from django.urls import path, include
from . import view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('log_in/',view.log_in,name='log_in'),
    path('registration/',view.registration,name='registration'),
    path('home/',view.home,name='home'),
    path('profile/',view.profile,name='profile'),
    path('profile/edit/', view.profile_edit, name='profile_edit'), # Added URL for profile edit
    path('log_out/',view.log_out,name='log_out'),
    path('accrequest/',view.accrequest,name='accrequest'),
    path('attrequest/',view.attrequest,name='attrequest'),
    path('myemployee/',view.myemployee,name='myemployee'),
    path('dashboard/',view.dashboard,name='dashboard'),
    path('view_details/<int:id>/<int:from_page>',view.view_details, name='view_details'),
    path('request_response/<str:username>/<str:action>',view.request_response, name='request_response'),
    path('attendance_submit/<str:username>/<str:action>',view.attendance_submit, name='attendance_submit'),
    path('update_attendance/<str:id>/<str:action>',view.update_attendance, name='update_attendance'),
    path('edit_attendance/<str:id>/<str:action>',view.edit_attendance, name='edit_attendance'),
    path('edit_active_status/<str:username>',view.edit_active_status, name='edit_active_status'),
    path('add_holiday/',view.add_holiday,name='add_holiday'),
    path('boss_edit/<int:id>/', view.boss_edit, name='boss_edit'),
    path('boss_edit_page/<int:id>/', view.boss_edit_page, name='boss_edit_page'),
    # path('export-to-excel/', view.export_attendance_to_excel, name='export_attendance_to_excel'),


    # URL's for the Subordinate
    path('subordinate_home/',view.subordinate_home,name='subordinate_home'),
    path('subordinate_profile/',view.subordinate_profile,name='subordinate_profile'),
    path('subordinate_profile/edit/', view.subordinate_profile_edit, name='subordinate_profile_edit'),
    path('subordinate_dashboard/',view.subordinate_dashboard,name='subordinate_dashboard'),
    path('subordinate_attendance_submit/<str:username>/<str:action>',view.subordinate_attendance_submit, name='subordinate_attendance_submit'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
