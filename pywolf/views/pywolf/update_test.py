from django.http import HttpResponseRedirect
from django.urls import reverse

from ...common.update import update


def update_test(village_no, day_no):
    update(village_no, day_no)
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no + 1,)))
