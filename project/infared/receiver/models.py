from django.db import models


class IRCodeInfo(models.Model):
    bit_count = models.IntegerField(max_length=2, blank=True, null=True)
    encoding = models.IntegerField(max_length=2, blank=True, null=True)
    length = models.IntegerField(max_length=2, blank=True, null=True)
    gap = models.IntegerField(max_length=10, blank=True, null=True)
    trail = models.IntegerField(max_length=3, blank=True, null=True)
    
    repeat = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True)
    header = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True)
    zero = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True)
    one = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True)

    min_repeat = models.IntegerField(max_length=3, blank=True, null=True)
    carrier_frequency = models.IntegerField(max_length=30, blank=True, null=True)
    duty_cycle = models.IntegerField(max_length=5, blank=True, null=True)
    
    # toggle_mask 
    
    def __unicode__(self):
        return "%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, " % (
                                            self.encoding,
                                            self.length,
                                            self.bit_count,
                                            self.gap,
                                            self.trail,
                                            self.header, 
                                            self.zero,
                                            self.one,
                                            self.min_repeat,
                                            self.carrier_frequency, 
                                            self.duty_cycle,
                                            # self.toggle_mask,
                                            self.repeat,
                                        )
    def dump_obj(self):
        o = {
                'encoding': self.encoding,
                'length': self.length,
                'bit_count': self.bit_count,
                'gap': self.gap, 
                'trail': self.trail,
                'header': self.header,
                'zero': self.zero,
                'one': self.one,
                'min_repeat': self.min_repeat,
                'carrier_frequency': self.carrier_frequency, 
                'duty_cycle': self.duty_cycle,
                }
        return o
        
    
    def load_codeinfo(self, code_info={}):        
        self.encoding = code_info.Encoding
        self.length = code_info.Length
        self.bit_count = code_info.BitCount
        self.gap= code_info.Gap
        self.trail = code_info.Trail
        self.header = ', '.join([str(i) for i in code_info.Header])
        self.zero = ', '.join([str(i) for i in code_info.Zero])
        self.one = ', '.join([str(i) for i in code_info.One])
        self.min_repeat = code_info.MinRepeat
        self.carrier_frequency = code_info.CarrierFrequency
        self.duty_cycle = code_info.DutyCycle
        # self.toggle_mask = code_info.ToggleMask
        self.repeat = ', '.join([str(i) for i in code_info.Repeat])
        
        return self


# Create your models here.
class IRCode(models.Model):
    #code_info = models.
    #bit_count
    #data
    #count 
    #e.codeInfo, e.code.BitCount, e.code.Data
    code_info = models.ForeignKey(IRCodeInfo)
    name = models.TextField(max_length=255, blank=True, null=True)
        