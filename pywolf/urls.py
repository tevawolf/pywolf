from django.urls import path

from .views.pywolf.index import index
from .views.pywolf.village import village
from .views.pywolf.create_village import create_village
from .views.pywolf.confirm_create_village import confirm_create_village
from .views.pywolf.exe_create_village import exe_create_village
from .views.pywolf.confirm import confirm
from .views.pywolf.voice import voice
from .views.pywolf.login import login
from .views.pywolf.logout import logout
from .views.pywolf.vote import vote
from .views.pywolf.entry import entry
from .views.pywolf.fortune import fortune
from .views.pywolf.assault import assault
from .views.pywolf.entry_cancel import entry_cancel
from .views.pywolf.selectstyle import selectstyle
from .views.pywolf.update_test import update_test

app_name = 'pywolf'
urlpatterns = [
    path('update_test/village<int:village_no>/day<int:day_no>', update_test, name='update_test'),
    path('', index, name='index'),
    path('create_village/', create_village, name='create_village'),
    path('confirm_create_village/', confirm_create_village, name='confirm_create_village'),
    path('execute_create_village/', exe_create_village, name='exe_create_village'),
    path('selectstyle/village<int:village_no>/day<int:day_no>', selectstyle, name='selectstyle'),
    path('village<int:village_no>/day<int:day_no>/', village, name='village'),
    path('village<int:village_no>/day<int:day_no>/confirm/', confirm, name='confirm'),
    path('village<int:village_no>/day<int:day_no>/voice/', voice, name='voice'),
    path('village<int:village_no>/day<int:day_no>/login/', login, name='login'),
    path('village<int:village_no>/day<int:day_no>/logout/', logout, name='logout'),
    path('village<int:village_no>/day<int:day_no>/selectstyle/', selectstyle, name='selectstyle'),
    path('village<int:village_no>/day<int:day_no>/vote/', vote, name='vote'),
    path('village<int:village_no>/day<int:day_no>/fortune/', fortune, name='fortune'),
    path('village<int:village_no>/day<int:day_no>/assault/', assault, name='assault'),
    path('village<int:village_no>/entry/', entry, name='entry'),
    path('village<int:village_no>/entry_cancel/', entry_cancel, name='entry_cancel'),
]