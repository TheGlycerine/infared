# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from infared.phidgets.ir import IRDevice
from infared.receiver.models import IRCodeInfo


def context(request): 
    return {}

def ird_receive(e):
    o = {}
    # Code is comming
    if e.repeat:
        o['message'] = 'Found Code' 
        bit_count = e.code.BitCount
        data = e.code.Data #list
        
        try:
            llc = e.device.getLastLearnedCode()
        except:
            llc = None

        if llc:
            print "STORE CODE", llc.Code.toString()    
            ir_code_info = IRCodeInfo().load_codeinfo(llc.CodeInfo)
            #ir_code_info
            c = IRCodeInfo.objects.filter(**ir_code_info.dump_obj()).count()
            # print ir_code_info
            if c <= 0:
                o['message'] = 'Code Known'
            else:
                ir_code_info.save()
                o['message'] = 'Learning Code'
        
            #print o['message'] #dir(e.device)

def index(request):
    
    ird = IRDevice(121774)
    # ird.responder = True
    ird.receive = ird_receive
    
    attached = ird.is_attached()
    
    return render_to_response('receiver/index.html', {'attached': attached}, context_instance=RequestContext(request, processors=[context]))