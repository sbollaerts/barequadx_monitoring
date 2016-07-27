from Receiver import Receiver

RX_PORT = 3  # Using UART(3) -> Pin Y10 (RX)
RX_SPEED = 115200  # 115200 bps is the standard speed although the RX module supports 125000 bps
DEBUG = True  # Used to display what the receiver object catches

receiver = None  # Useless, but I like to declare all my variables on top of my code
input_min = [2048] * 4  # All the minimum value received by channel (we only care about the 1st four channels)
input_max = [0] * 4  # All maximum values received by channel
input_value = [0] * 4  # All last values received by channel

output_min = [2048] * 4  # Weighted minimum values
output_max = [2048] * 4  # Weighted maximum values
output_neutral = [0] * 4  # Neutral values saved at startup (assuming all sticks are in central position when starting)


def compute_rate(range_min, range_max, value):
    """This function computes the rate of a value within a range."""
    if range_max == range_min:  # Avoid any division by zero
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

# Instantiate the receiver object
receiver = Receiver(port=RX_PORT, speed=RX_SPEED, debug=False)

# Main loop: record all values and adapt the ranges per channel
try:
    while True:
        if receiver.read_serial():
            for i in range(0, 4):
                if receiver.channels[i] > 0:
                    # Save the received value and adapt the boundaries if necessary
                    input_value[i] = receiver.channels[i]
                    input_min[i] = min(input_min[i], input_value[i])
                    input_max[i] = max(input_max[i], input_value[i])

                    # Save the first value for each channel as the neutral position
                    if output_neutral[i] == 0:
                        output_neutral[i] = input_value[i]

                    # Determine the delta between the neutral and the boundaries
                    delta_low = output_neutral[i] - input_min[i]
                    delta_high = input_max[i] - output_neutral[i]
                    delta = min(delta_low, delta_high)

                    # Define the new boundaries with the smallest delta
                    output_min[i] = output_neutral[i] - delta
                    output_max[i] = output_neutral[i] + delta

                # Display information per channel (raw + calculated)
                print("CH%d [%d<%4d<%d] %3d%% - (%d:%d) %3d%%" % (
                    i,
                    input_min[i], input_value[i], input_max[i],
                    compute_rate(input_min[i], input_max[i], input_value[i]),
                    output_min[i], output_max[i],
                    compute_rate(output_min[i], output_max[i], input_value[i])), end=" || ")
            print("")
except KeyboardInterrupt:  # Catch the [CTRL]+[C] in REPL
    receiver = None
