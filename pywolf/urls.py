from django.urls import path

from .views.pywolf.index import index
from .views.pywolf.village import village
from .views.pywolf.confirm import confirm
from .views.pywolf.voice import voice
from .views.pywolf.login import login
from .views.pywolf.logout import logout
from .views.pywolf.vote import vote
from .views.pywolf.entry import entry
from .views.pywolf.fortune import fortune
from .views.pywolf.entry_cancel import entry_cancel
from .views.pywolf.selectstyle import selectstyle

app_name = 'pywolf'
urlpatterns = [
    path('', index, name='index'),
    path('selectstyle/int:village_no><int:day_no>', selectstyle, name='selectstyle'),
    path('village<int:village_no>/day<int:day_no>/', village, name='village'),
    path('village<int:village_no>/day<int:day_no>/confirm/', confirm, name='confirm'),
    path('village<int:village_no>/day<int:day_no>/voice/', voice, name='voice'),
    path('village<int:village_no>/day<int:day_no>/login/', login, name='login'),
    path('village<int:village_no>/day<int:day_no>/logout/', logout, name='logout'),
    path('village<int:village_no>/day<int:day_no>/selectstyle/', selectstyle, name='selectstyle'),
    path('village<int:village_no>/day<int:day_no>/vote/', vote, name='vote'),
    path('village<int:village_no>/day<int:day_no>/fortune/', fortune, name='fortune'),
    path('village<int:village_no>/entry/', entry, name='entry'),
    path('village<int:village_no>/entry_cancel/', entry_cancel, name='entry_cancel'),
]