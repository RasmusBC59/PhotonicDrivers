
import time
import serial


# Found in the following github https://github.com/vuthalab/thorlabs-rotation_mount?tab=readme-ov-file

def from_twos_complement(n, bits=32):
    if n < (1 << (bits-1)): return n
    return n - (1 << bits)

def to_twos_complement(n, bits=32):
    return (1 << bits) + n if n < 0 else n


# Encoder counts per revolution (from manual)
COUNTS_PER_REVOLUTION = 143360

# List of status responses
RESPONSES = [
    'ok',
    'communication timeout',
    'mechanical timeout',
    'command error',
    'value out of range',
    'module isolated',
    'module out of isolation',
    'initialization error',
    'thermal error',
    'busy',
    'sensor error',
    'motor error',
    'out of range',
    'overcurrent',
]

class ElliptecRotationStage:
    def __init__(
            self,
            serial_connection, 
            address: int, # Device address on controller bus.
            offset: int, # Software angle offset, in encoder counts.
        ):
        self._conn = serial_connection
        self.address = address
        self._offset = offset

    def send(self, command, data=b''):
        """Send the given command type, with the given data payload."""
        packet = (
            str(self.address).encode('utf-8')
            + command.encode('utf-8')
            + data.hex().upper().encode('utf-8')
            + b'\n'
        )
        self._conn.write(packet)

    def query(self, command, data=b''):
        """
        Send the given command type, with the given data payload.
        Return the response type and decoded data payload from the Elliptec controller.
        """
        self.send(command, data=data)

        response = b''
        while True:
            response += self._conn.read(8192)
            if response.endswith(b'\r\n'): break
            time.sleep(0.2)

        header, data = response[:3], response[3:-2]
        assert chr(header[0]) == str(self.address)
        return header[1:].decode(), int(data.decode(), 16)


    ##### Debug/Internal Commands ######
    @property
    def status(self):
        header, response = self.query('gs')
        assert header == 'GS'
        return RESPONSES[response]

    @property
    def _position(self):
        header, response = self.query('gp')
        assert header == 'PO'
        return from_twos_complement(response)


    ##### Public Interface #####
    def home(self):
        """
        Return the stage to the home position.
        (May correspond to 0 degrees in software.)
        """
        self.query('ho')

    def tare(self):
        """Mark the current position as 0° in software."""
        self._offset = -self._position

    @property
    def angle_unwrapped(self):
        """Return the current angle (CCW), counting full turns."""
        return -360 * (self._position + self._offset) / COUNTS_PER_REVOLUTION

    @angle_unwrapped.setter
    def angle_unwrapped(self, degrees):
        self.move_by(degrees - self.angle_unwrapped)

    @property
    def angle(self):
        """Return the current angle (CCW)."""
        return self.angle_unwrapped % 360

    @angle.setter
    def angle(self, degrees):
        delta = degrees - self.angle
        if delta > 180: delta -= 360
        if delta < -180: delta += 360

        self.move_by(delta)
        
    def set_angle(self, degrees):
        delta = degrees - self.angle
        if delta > 180: delta -= 360
        if delta < -180: delta += 360

        self.move_by(delta)

    def move_by(self, degrees):
        """Move by the given number of degrees, counterclockwise."""
        delta = -round(degrees * COUNTS_PER_REVOLUTION/360)
        data = to_twos_complement(delta).to_bytes(4, 'big')
        header, response = self.query('mr', data=data)
        assert header in ['GS', 'PO']
        if header == 'GS': raise ValueError(RESPONSES[response])



serial_connection = serial.Serial(port='COM8', baudrate=9600, stopbits=1, parity='N', timeout=0.05)
time.sleep(2)
QWP915c = ElliptecRotationStage(serial_connection=serial_connection, offset=-8529, address="A")
QWP915c.set_angle(90)
HWP915c = ElliptecRotationStage(serial_connection=serial_connection, offset=-8529, address="B")
HWP915c.set_angle(0)
QWP915c = ElliptecRotationStage(serial_connection=serial_connection, offset=-8529, address="C")
QWP915c.set_angle(90)
HWP915c = ElliptecRotationStage(serial_connection=serial_connection, offset=-8529, address="D")
HWP915c.set_angle(0)

serial_connection.close()