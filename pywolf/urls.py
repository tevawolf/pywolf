from django.urls import path

from .views.pywolf.index import index
from .views.pywolf.village import village
from .views.pywolf.create_village.create_village import create_village
from .views.pywolf.create_village.confirm_create_village import confirm_create_village
from .views.pywolf.create_village.exe_create_village import exe_create_village
from .views.pywolf.confirm_voice import confirm_voice
from .views.pywolf.voice import voice
from .views.pywolf.login import login
from .views.pywolf.login.logout import logout
from .views.pywolf.ability.vote import vote
from .views.pywolf.entry import entry
from .views.pywolf.ability.fortune import fortune
from .views.pywolf.ability.assault import assault
from .views.pywolf.entry.entry_cancel import entry_cancel
from .views.pywolf.selectstyle import selectstyle
from .views.pywolf.update_test import update_test
from .views.pywolf.create_user import create_user
from .views.pywolf.create_user.confirm_create_user import confirm_create_user
from .views.pywolf.create_user.exe_create_user import exe_create_user

app_name = 'pywolf'
urlpatterns = [
    path('create_user/effebf1b7d7e1f715183405fbbb8a8b10/', create_user, name='create_user'),
    path('confirm_create_user/effebf1b7d7e1f715183405fbbb8a8b10/', confirm_create_user, name='confirm_create_user'),
    path('execute_create_user/effebf1b7d7e1f715183405fbbb8a8b10/', exe_create_user, name='exe_create_user'),
    path('update_test/village<int:village_no>/day<int:day_no>', update_test, name='update_test'),
    path('', index, name='index'),
    path('create_village/', create_village, name='create_village'),
    path('confirm_create_village/', confirm_create_village, name='confirm_create_village'),
    path('execute_create_village/', exe_create_village, name='exe_create_village'),
    path('selectstyle/village<int:village_no>/day<int:day_no>', selectstyle, name='selectstyle'),
    path('village<int:village_no>/day<int:day_no>/', village, name='village'),
    path('village<int:village_no>/day<int:day_no>/confirm_voice/', confirm_voice, name='confirm_voice'),
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