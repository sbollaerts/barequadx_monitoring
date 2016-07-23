# ############################################################################
# CLASS: Receiver
#
# ROLE: Responsible for reading and parsing commands sent by the receiver
#       module
#
# USAGE:
#    - __init__(port=3, speed=25000): initialize a new instance of this class
#         and open the serial communication on the given port at the given speed
#    - The read_serial() function is called to read data from the serial and
#         parse it. Data is read by packet of 16 bytes.
#
# REMARKS:
#    - This class is bound to the specific receiver "Spektrum DSMX quad race
#      receiver with diversity (SPM4648)"
#    - This class has been elaborated based on the official Spektrum info
#      "Spektrum Remote Receiver Interfacing" available at http://bit.ly/1Z96ARL
# ############################################################################
from pyb import UART


class Receiver:
    # Allowed System Field values
    _DSM2_1024_22MS = 0x01
    _DSM2_2048_11MS = 0x12
    _DSMS_2048_22MS = 0xa2
    _DSMX_2048_11MS = 0xb2
    _SYSTEM_FIELD_VALUES = (_DSM2_1024_22MS, _DSM2_2048_11MS, _DSMS_2048_22MS, _DSMX_2048_11MS)

    # Channel formats depending on system field value
    _MASK_1024_CHANID = 0xFC00  # when 11ms
    _MASK_1024_SXPOS = 0x03FF  # when 11ms
    _MASK_2048_CHANID = 0x7800  # when 22ms
    _MASK_2048_SXPOS = 0x07FF  # when 22ms

    # Serial configuration
    _uart = None
    _uart_port = 0  # Which UART port to use?
    _uart_speed = 0  # Which UART speed to use?

    # Serial buffer and frame data
    _system_field = None
    _frame = [0] * 16  # Assumption: frames are received correctly, no need of intermediate buffer and controls
    _channels = [0] * 20  # Up-to 20 channels can be used by SPM4648

    _debug = None

    # ########################################################################
    # ### Properties
    # ########################################################################
    @property
    def port(self):
        return self._uart_port

    @property
    def speed(self):
        return self._uart_speed

    @property
    def frame(self):
        return self._frame

    @property
    def channels(self):
        return self._channels

    @property
    def system_field(self):
        return self._system_field

    # ########################################################################
    # ### Constructor and destructor
    # ########################################################################
    def __init__(self, port, speed, debug=False):
        self._debug = debug
        self._uart_port = port
        self._uart_speed = speed
        self._uart = UART(self._uart_port, self._uart_speed)

    # ########################################################################
    # ### Functions
    # ########################################################################
    def read_serial(self):
        # Lire un frame
        if self._uart.any():
            index = 0
            while index < 16:
                self._frame[index] = self._uart.readchar()
                index += 1
            self._decode_frame()
            return True
        else:
            return False

    def _decode_frame(self):
        # Verify the system field (_channels[2])
        if self._frame[1] in self._SYSTEM_FIELD_VALUES:
            self._system_field = self._frame[1]
            if self._frame[1] == self._DSM2_1024_22MS:
                for i in range(1, 7):
                    data = self._frame[i * 2] * 256 + self._frame[(i * 2) + 1]
                    channel = (data & self._MASK_1024_CHANID) >> 10
                    value = data & self._MASK_1024_SXPOS
                    self._channels[channel] = value
            else:
                for i in range(1, 7):
                    data = self._frame[i * 2] * 256 + self._frame[(i * 2) + 1]
                    channel = (data & self._MASK_2048_CHANID) >> 11
                    value = data & self._MASK_2048_SXPOS
                    self._channels[channel] = value
        else:
            pass  # Invalid system field value -> Do nothing

        if self._debug:
            self.debug()

    def debug(self):
        if not self._debug:
            return

        print("RX  OUT: ", end="")
        for i in range(0, 4):
            print("CH%2d: %4d" % (i, self._channels[i]),
                  end=" || ")
        print("")
