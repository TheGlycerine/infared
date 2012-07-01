# Auto Generated with make_admin
# ######################################################## #
# YOU MUST DELETE THE ABOVE STATEMENT                      #
# IF YOU DO NOT WANT ./manage.py change_model <model_name> #
# TO REGENERATE THIS admin.py                              #
# YOUR CHANGES WILL BE OVERWRITTEN                         #
############################################################

from django.contrib import admin
from models import IRCode, IRCodeInfo

class IRCodeAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()
    #fields = ()
    filter_horizontal = ()
    #exclude = (,)

class IRCodeInfoAdmin(admin.ModelAdmin):
    list_display = ('bit_count', 'encoding', 'length', 'gap', 'trail', 'repeat', 'header', 'zero', 'one', 'min_repeat', 'carrier_frequency', 'duty_cycle', )
    list_filter = ('bit_count', 'encoding', 'length', 'gap', 'trail', 'repeat', 'header', 'zero', 'one', 'min_repeat', 'carrier_frequency', 'duty_cycle', )
    search_fields = ('bit_count', 'encoding', 'length', 'gap', 'trail', 'repeat', 'header', 'zero', 'one', 'min_repeat', 'carrier_frequency', 'duty_cycle', )
    #fields = ('bit_count', 'encoding', 'length', 'gap', 'trail', 'repeat', 'header', 'zero', 'one', 'min_repeat', 'carrier_frequency', 'duty_cycle', )
    filter_horizontal = ()
    #exclude = (,)



admin.site.register(IRCode, IRCodeAdmin)
admin.site.register(IRCodeInfo, IRCodeInfoAdmin)

