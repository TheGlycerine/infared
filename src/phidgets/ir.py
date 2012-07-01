from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from Phidgets.Devices.IR import IR, IRCode, IRCodeInfo, IRCodeLength, IREncoding
try:
    import winsound
    win_sound = True
except: 
    sys.stdout.write('Windows sound cannot be used')
    win_sound = False
    
class IRDevice(object):
    
    def __init__(self, sn=1010101, ir_class=None, 
                 wait_time=10000, codes=[], auto=True,
                 listen=True, respond=False
                 ):
        
        # The IRDA Device serial number
        self.sn = sn
        self.last_event = None
        # A list of stored codes whilst the
        # IRDA device is connected through
        # this class.
        self.codes = codes
        if self.sn == 1010101:
            self.output("You must add your own unique serial \
            number for this device")
        
        # Time taken for device connection failure.
        self.wait_time = wait_time
        
        # The Phidgets.Devices.IR class
        if ir_class is None: ir_class = IR()
        self._IR = ir_class 
        
        # If the device is allowed to connect to
        # immediately.
        # If the serial number has been passed
        if auto is True and sn !=  1010101:
            self.attach()
        
        self.listen = listen
        self.respond = respond
    
    
    
    def receive(self, e):
        '''
        IRDA Signal hook
        '''
        if win_sound:
            winsound.PlaySound("*", winsound.SND_ALIAS)
    
    def respond(self, e):
        '''
        automatic respond hook
        '''
        pass
    
    
    # Begin using the object.
    def attach(self, sn=None):
        if sn: self.sn = sn
        
        try:
            self._IR.openPhidget(self.sn)
            if win_sound:
                winsound.PlaySound("*", winsound.SND_ALIAS)
        except:
            self.output('Could not open widget')
            return False

        try:
            self._IR.waitForAttach(self.wait_time)
        except:
            self.output('Could not attach to device. Ensure \
you have the device plugged in and turned on, the serial number \
is correct and no other application is accessing the device.')
            return False
        self.attach_handlers()
        return True
    
    def detach(self):
        if self._IR:
            self.output("Closing %d" % self._IR.getSerialNum())
        try:
            self._IR.closePhidget()
            if win_sound:
                winsound.PlaySound("*", winsound.SND_ALIAS)
        except:
            self.output("Failed to close IRDevice. \
It may be still connected!")
           
    
    '''
    Hook for phidget release
    '''
    close = detach
    
    @property  
    def responder(self):
        return self._responder

    @responder.setter
    def responder(self, b):
        self.listen_respond(b)
    
    def listen_respond(self, b):
        """
        Listen Respond assigns the funcationality
        of a repeater. If the device receives a code, it will
        be repeated.
        """
        print 'Listen Respond is %s' % b
        self.listen = b
        self.respond = b
        
    def output(self, *args):
        for x in args: print x,
        print(' ')
        
    #Event Handler Callback Functions
    def ir_attached(self, e):
        attached = e.device
        self.output("PhidgetIR %i Attached!" % 
                    (attached.getSerialNum())
                    )
    
    def ir_detached(self, e):
        detached = e.device
        self.output("PhidgetIR %i Detached!" % 
                    (detached.getSerialNum())
                    )
        self._IR.closePhidget()
    
    def ir_error(self, e):
        try:
            source = e.device
            self.output("PhidgetIR %i: Phidget Error %i: %s" %
                         (source.getSerialNum(), 
                          e.eCode, 
                          e.description)
                        )
        except PhidgetException as e:
            self.output("Phidget Exception %i: %s" % (e.code, 
                                                      e.details)
                        )
    
    def ir_code_recv(self, e):
        #print("Phiget IR Code Receive")
        if self.listen:
            self.receive(e)
            
            if e.repeat:
                repeat = True
            else:
                repeat = False
            self.output('Receive %s' % e.code.toString())
            
            if repeat:
                if self.respond:
                    code = None
                    if self.last_event:
                        code = self.last_event.code
                        
                    if code:
                        if code.Data == e.code.Data:
                            self.sendLastCode()
                            self.output("Respond %s" % e.code.toString())
                    
                else:
                    self.output("Receive code %s" % e.code.toString())
                    
                

    
    def sendLastCode(self):
        '''
        A safe method to repeat the last
        learnt transmission.
        if the last code is not know, 
        thia will silently fail returning
        false.
        '''
        if self.last_event:
            self.transmit_event(self.last_event)
            return self.last_event
        return False
    
    def ir_learn_recv(self, e):
        '''
        New code learn
        '''
        if e not in self.codes:
            self.last_event = e
            self.codes.append(e)
            self.output("Learned:", e.code.toString())
    
    def ir_raw_data_recv(self,e):
        pass
    
    def transmit_event(self, e):
        if self.is_attached():
            self.transmit(e.codeInfo, e.code.BitCount, e.code.Data)
        
    def transmit(self, code_info, bit_count=32, data=None):
        irc = IRCode(data, bit_count)
        self._IR.transmit(irc, code_info)
    
    def is_attached(self):
        '''
        Is the device attached
        '''
        return self._IR.isAttached()
    
    def __str__(self):
        return "<Phidget.IRDevice %s attached: %s>" % (self.sn, 
                                                self.is_attached())
    
    __repr__ = __str__ 
    

    def attach_handlers(self,
                        attach_handler=ir_attached,
                        detach_handler=ir_detached,
                        error_handler=ir_error,
                        ir_code_handler=ir_code_recv,
                        ir_learn_handler=ir_learn_recv,
                        ir_raw_data_handler=ir_raw_data_recv):
        
        # Attach the IRDA handlers internally by passing
        # a self reference from within the class. This
        # keeps the scope tidy.

        self._IR.setOnAttachHandler(lambda x: 
                                    attach_handler(self, x)) 
        self._IR.setOnDetachHandler(lambda x: 
                                    detach_handler(self, x))
        self._IR.setOnErrorhandler(lambda x: 
                                   error_handler(self, x))
        self._IR.setOnIRCodeHandler(lambda x: 
                                    ir_code_handler(self, x))
        self._IR.setOnIRLearnHandler(lambda x: 
                                     ir_learn_handler(self, x))
        self._IR.setOnIRRawDataHandler(lambda x: 
                                       ir_raw_data_handler(self, x))
            
    
    