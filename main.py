from Receiver import Receiver

RX_PORT = 3
RX_SPEED = 115200
DEBUG = True

receiver = None
input_min = [2048] * 4
input_max = [0] * 4
input_value = [0] * 4

output_min = [2048] * 4
output_max = [2048] * 4
output_neutral = [0] * 4


def compute_rate(range_min, range_max, value):
    if range_min == 0 | range_max == range_min:
        rc = 0
    else:
        value = max(min(value, range_max), range_min)
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
                    input_value[i] = receiver.channels[i]
                    input_min[i] = min(input_min[i], input_value[i])
                    input_max[i] = max(input_max[i], input_value[i])

                    if output_neutral[i] == 0:
                        output_neutral[i] = input_value[i]

                    delta_low = output_neutral[i] - input_min[i]
                    delta_high = input_max[i] - output_neutral[i]
                    delta = min(delta_low, delta_high)

                    output_min[i] = output_neutral[i] - delta
                    output_max[i] = output_neutral[i] + delta

                print("CH%d [%d<%4d<%d] %3d%% - (%d:%d) %3d%%" % (
                    i,
                    input_min[i], input_value[i], input_max[i],
                    compute_rate(input_min[i], input_max[i], input_value[i]),
                    output_min[i], output_max[i],
                    compute_rate(output_min[i], output_max[i], input_value[i])), end=" || ")
            print("")
except KeyboardInterrupt:
    receiver = None
