from django.forms import ModelForm
from .models import service

class serviceForm(ModelForm):
    class Meta:
        model = service
        labels={'item':'உருப்படி','customer':'வாடிக்கையாளர் பெயர்','mobilenum':'கைபேசி எண்','description':'விளக்கம்','amount':'மொத்த தொகை','important':'முக்கியம்'}
        fields = ['item','customer','mobilenum','description','amount','important']