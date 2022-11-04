from django.contrib import admin

from .models import Vazhipadu, Data
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('vazhipadu', 'person_name', 'nakshathram', 'count', 'created_date')
    list_filter = ('vazhipadu', 'created_date')
    readonly_fields = ('vazhipadu', 'count', 'created_date', 'just_date')
    # search_fields = ['created_date']
    

class VazhipaduAdmin(admin.ModelAdmin):
    list_display = ('vazhipadu_name', 'price', 'created_date', 'modified_date')
    


admin.site.register(Vazhipadu, VazhipaduAdmin)
admin.site.register(Data, DataAdmin)
