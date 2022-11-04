from django.forms import NullBooleanField
from .models import Vazhipadu

def vazhipadukal(request):
    vazhipadu_rates = Vazhipadu.objects.all()
    return dict(vazhipadu_rates=vazhipadu_rates)
