from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from Phidgets.Devices.IR import IR, IRCode, IRCodeInfo, IRCodeLength, IREncoding

codes = []
last_msg = ''

def message(*args):
    global last_msg
    for x in args:
        if x == last_msg:
            print '.',
            return
        else: 
            print x, 
    
    print(' ')
    last_msg= x
        
#Event Handler Callback Functions
def irAttached(e):
    attached = e.device
    message("PhidgetIR %i Attached!" % (attached.getSerialNum()))

def irDetached(e):
    detached = e.device
    message("PhidgetIR %i Detached!" % (detached.getSerialNum()))

def irError(e):
    try:
        source = e.device
        message("PhidgetIR %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        message("Phidget Exception %i: %s" % (e.code, e.details))

def irCodeRecv(e):
    #print("Phiget IR Code Receive")
    source = e.device
    if e.repeat:
        repeat = True
    else:
        repeat = False
    
    if repeat:
        message("Receive code")
        # message("PhidgetIR %i Code Receive: Code: %s Repeat: %s" % (source.getSerialNum(), e.code.toString(), repeat))
    

def irLearnRecv(e):
    
    # The code info is important 
    # it is required to revalidate the ircode.
    # Json this object for db
    print 'CodeInfo'
    print dir(e.codeInfo)
    print '---'    
    # This is all you need from the close - 
    print 'code', e.code.toString()
    print 'Data', e.code.Data
    print 'BitCount', e.code.BitCount
    print '---'
    print dir(e.device)
    #e.device.closePhidget
    #e.device.disableLogging
    #e.device.getDeviceClass
    #e.device.getDeviceClass
    
    e.device.transmit(IRCode(e.code.Data, e.code.BitCount), e.codeInfo)
    
    source = e.device
    #print("PhidgetIR %i Learn Receive: Code: %s -- Code Info:" % (source.getSerialNum(), e.code.toString()))
    
    #displayCodeInfo(e.codeInfo)
    if e not in codes:
        codes.append(e)
        message("New code learned:", e.code.toString())
    
    
def irRawDataRecv(e):
    source = e.device
    
    #print("PhidgetIR %i Raw Data Received:" % (source.getSerialNum()))
    #displayRawData(e.rawData)

def displayRawData(data):
    message("----------------------------------------------------")
    outStr = "Raw Data:"
    for i in range(len(data)):
        if (i % 8) == 0: outStr += "\n"
        if data[i] == IR.RAWDATA_LONGSPACE:
            outStr += "LONG"
        else:
            outStr += str(data[i])
        if ((i + 1) % 8) != 0: outStr += ", "
    message("%s" % (outStr))
    message("----------------------------------------------------")
    
    
def displayCodeInfo(codeInfo):
    message("----------------------------------------------------")
    message("Bit Count: %d\nEncoding: %s\nLength: %s\nGap: %d\nTrail: %d" % (codeInfo.BitCount, IREncoding.toString(codeInfo.Encoding), IRCodeLength.toString(codeInfo.Length), codeInfo.Gap, codeInfo.Trail))
    if codeInfo.Header != None:
        message("Header: { %d, %d }" % (codeInfo.Header[0], codeInfo.Header[1]))
    else:
        message("Header: Null")
    message("One: { %d, %d }\nZero: { %d, %d }" % (codeInfo.One[0], codeInfo.One[1], codeInfo.Zero[0], codeInfo.Zero[1]))
    
    if codeInfo.Repeat != None:
        printStr = "{ "
        for i in range(len(codeInfo.Repeat)):
            if i > 0:
                printStr += ", "
            printStr += str(codeInfo.Repeat[i])
        printStr += " }"
        
        message("Repeat: %s" % (printStr))
    else:
        message("Repeat: None")
    
    message("MinRepeat: %d\nToggle Mask: %s\nCarrier Frequency: %d\nDuty Cycle: %d" % (codeInfo.MinRepeat, codeInfo.ToggleMask.toString(), codeInfo.CarrierFrequency, codeInfo.DutyCycle))
    message("----------------------------------------------------")


try:
    interfaceKit = InterfaceKit()
    message( "Setting up interface", interfaceKit)
    ir = IR()
except RuntimeError as e:
    print("Runtime Error: %s" % e.message)

try:
    try:
        message( "Opening IR Device 121774")
        ir.openPhidget(121774)
        message( "Waiting for attachment...")
        ir.waitForAttach(10000)
        message("Device ready.")
        ir.setOnAttachHandler(irAttached)
        ir.setOnDetachHandler(irDetached)
        ir.setOnErrorhandler(irError)
        ir.setOnIRCodeHandler(irCodeRecv)
        ir.setOnIRLearnHandler(irLearnRecv)
        ir.setOnIRRawDataHandler(irRawDataRecv)
        
        try:
            message("Device ready and waiting...")
            while True:
                pass
        except KeyboardInterrupt as e:
            message("Exiting")
        
    except PhidgetException as e:
        message("Phidget Exception %i: %s" % (e.code, e.details))
        message("Exiting....")
finally:
    if ir:
        message ("Closing %d" % (interfaceKit.getSerialNum()))
    interfaceKit.closePhidget()

