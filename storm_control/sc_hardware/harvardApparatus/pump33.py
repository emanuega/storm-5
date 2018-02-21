'''
A class for interfacing with Pump 33 from Harvard Apparatus

TODO: Implement control for the second pump independently 

George Emanuel
2/17/2108
'''

import serial
import enum

class PumpDirection(enum.Enum):
    Infuse = 'INF'
    Refill = 'REF'
    Reverse = 'REV'

class PumpMode(enum.Enum):
    AutoStop = 'AUT'
    Proportional = 'PRO' 
    Continuous = 'CON'

class PumpState(enum.Enum):
    Stopped = enum.auto()
    Infusing = enum.auto()
    Refilling = enum.auto()
    Stalled = enum.auto()


class Pump33():

    def __init__(self, com_port='COM2', pump_address = 1, baudrate = 9600):
        self.pump_address = 1
        self.serial = serial.Serial(port = com_port, 
                baudrate = baudrate, timeout = 0.5, 
                bytesize=serial.EIGHTBITS,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_TWO)

    def getRate(self):
        return self._writeAndRead('RAT').split('\r')[0].strip('\n')

    def setRate(self, rate):
        '''Set the rate of the syringe pump in ul/min'''

        response = self._writeAndRead('RAT ' + '{:.5g}'.format(rate) + ' UM')

        if 'OOR' in response:
            raise ValueError(
                    'Pump33 rate value ' + str(rate) + ' out of range')

    def getDiameter(self):
        '''Get the syringe diameter in mm as a float'''

        return float(self._writeAndRead('DIA').split('\r')[0].strip('\n'))

    def setDiameter(self, diameter):
        '''Set the syringe diameter in mm
        
        If the pump is running, it is stopped before setting the diameter
        '''

        self.stop()
        response = self._writeAndRead('DIA ' + '{:5g}'.format(diameter))

        if 'OOR' in response:
            raise ValueError(
                    'Pump33 diameter value ' + str(diameter) + ' out of range')


    def getStatus(self):
        '''Returns the current state of the pump 
        
        The pump state is either Stopped, Infusing, Refilling, or Stalled.'''
        response = self._writeAndRead('')

        if ':' in response:
            return PumpState.Stopped
        elif '>' in response:
            return PumpState.Infusing
        elif '<' in response:
            return PumpState.Refilling
        elif '*' in response:
            return PumpState.Stalled

    def getMode(self):
        '''Get the pumping mode (auto stop, proportional, or continuous)
        
        auto stop - Both syringes pump according to diameter 1 and rate 1
        until syring 1 reaches limit switch
        proportional - Each syringe pumps independently with the corresponding
        diameters and rates until syringe 1 reaches the limit switch
        continuous - Both syringes pump according to diameter 1 and rate 1.
        When syringe 1 reaches the limit switch, the direction of both 
        syringes is reversed.
        '''

        return PumpMode(self._writeAndRead('MOD').split('\r')[0].strip('\n'))

    def setMode(self, mode):
        '''Set the pumping mode to auto stop, proportional, or continuous'''

        self._writeAndRead('MOD ' + mode.value)
        

    def getDirection(self):
        '''Get the direction of the pump

        The returned direction is either 'INFUSE' or 'REFILL'
        '''

        return self._writeAndRead('DIR').split('\r')[0].strip('\n')

    def setDirection(self, direction):
        '''Set the direction of the syringe pump'''

        self._writeAndRead('DIR ' + direction.value)

    def reverse(self):
        '''Reverse the directiotn of the syringe pump'''

        self._writeAndRead('DIR ' + PumpDirection.Reverse.value)

    def setParallel(self, parellel):
        '''Sets the syringe pumps to act in parallel or reciprocal mode'''

        if parallel:
            self._writeAndRead('PAR ON')
        else:
            self._writeAndRead('PAR OFF')

    def run(self):
        self._writeAndRead('RUN')

    def stop(self):
        self._writeAndRead('STP')

    def pumpVersion(self):
        '''Requests the pump version.''' 

        return self._writeAndRead('VER').split('\r')[0].strip('\n')

    def _writeAndRead(self, message):
        self._write(message)
        return self._read()

    def _write(self, message):
        appendedMessage = message + '\r'
        self.serial.write((str(self.pump_address) + appendedMessage).encode())

    def _read(self):
        inMessage = self.serial.read(64).decode()
        return inMessage

