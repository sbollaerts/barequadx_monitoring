from Receiver import Receiver

RX_PORT = 3
RX_SPEED = 115200
DEBUG = True

receiver = None
range_min = [2048] * 4
range_max = [0] * 4
range_neutral = [1024] * 4
range_value = [0] * 4


def compute_rate(range_min, range_max, value):
    if range_min == 0 | range_max == range_min:
        rc = 0
    else:
        rc = ((value - range_min) / (range_max - range_min)) * 100
    return rc


print("**************************************************************************")
print("*** Bare Quad X - Monitoring Tool                                      ***")
print("***                                                                    ***")
print("*** Purpose                                                            ***")
print("***    - Determine the min, max, neutral values                        ***")
print("***    - Display the current value and compare it to the neutral value ***")
print("**************************************************************************")

receiver = Receiver(port=RX_PORT, speed=RX_SPEED, debug=False)

try:
    while True:
        if receiver.read_serial():
            for i in range(0, 4):
                if receiver.channels[i] > 0:
                    range_value[i] = receiver.channels[i]
                    range_min[i] = min(range_min[i], range_value[i])
                    range_max[i] = max(range_max[i], range_value[i])
                    range_neutral[i] = range_min[i] + (range_max[i] - range_min[i]) / 2
                print("CH%.2d [%4d:%4d] (%4d) %4d -> %3d%%" % (
                    i, range_min[i], range_max[i], range_neutral[i], range_value[i],
                    compute_rate(range_min[i], range_max[i], range_value[i])), end=" || ")
            print("")
except KeyboardInterrupt:
    receiver = None
