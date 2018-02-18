'''
A class for interfacing with Pump 33 from Harvard Apparatus

George Emanuel
2/17/2108
'''

import serial

class PumpDirection(Enum):
    Infuse = 'INF'
    Refill = 'REF'
    Reverse = 'REV'

class PumpMode(Enum):
    AutoStop = 'AUT'
    Proportional = 'PRO' 
    Continuous = 'CON'

class Pump33():

    def __init__(self, com_port='COM2'):
        self.com_port = com_port
        self.serial = serial.Serial(port = self.com_port, 
                baudrate = 9600, timeout = 0.5)

    def setRate(self, rate):
        '''Set the rate of the syringe pump in ul/min'''

        self.write('RAT ' + '{:.6g}'.format(rate) + ' UM')

    def setDiameter(self, diameter):
        '''Set the syringe diameter in mm'''

        self.write('DIA ' + '{:6g}'.format(diameter))


    def setMode(self, mode):
        '''Set the pumping mode to auto stop, proportional, or continuous'''

        self.write('MOD ' + mode.value)
        

    def getDirection(self):
        '''Get the direction of the pump

        The returned direction is either 'INFUSE' or 'REFILL'
        '''

        self.write('DIR')
        return self.read()

    def setDirection(self, direction):
        '''Set the direction of the syringe pump'''

        self.write('DIR ' + direction.value)

    def setParallel(self, parellel):
        '''Sets the syringe pumps to act in parallel or reciprocal mode'''

        if parallel:
            self.write('PAR ON')
        else:
            self.write('PAR OFF')

    def run(self):
        self.write('RUN')

    def stop(self):
        self.write('STP')

    def pumpVersion(self):
        '''Requests the pump version. This should be 33V1.0'''

        self.write('VER')
        return self.read()

    def write(self, message):
        appendedMessage = message + '\r'
        self.serial.write(appendedMessage.encode())

    def read(self):
        inMessage = self.serial.readline().decode().rstrip()
        return inMessage

