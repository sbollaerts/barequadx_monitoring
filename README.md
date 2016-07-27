# Bare Quad X - Monitoring and Configuration Utility
The purpose of this tool is to check the inputs of the RX module and produce a configuration file defining value ranges for each channel. 

### Usage
- Position both stick in neutral (centre position)
- Switch the device ON
- Switch the radio ON
- Move each stick on all directions
- When finished, press simultaneously on \[CTRL\]+\[C\]
- A configuration file (configuration.cfg) will be produced: this file should be used with the BareQuadX firmware

### How does it work?
The theoretical range for each channel is \[0:2048\[ with the Spektrum DSMX Quad Race Receiver with Diversity. In the reality, the range is smaller. Based on the official documentation of Spektrum RX, the range should be \[341:1707\]. In the reality, this range can vary: for example, my throttle range is \[142:1694\], while other are roughy \[345:1705\].
Considering the neutral position, it should be located in the middle of the range. For example, the neutral could be determined with min+(max-min)/2:

- \[0:2048\[: 1024
- \[142:1694\]: 918
- \[345:1705\]: 1025

After some tests I discovered that the neutral values were not the ones expected; leading to errors that might cause serious damages. Amongst all possibilities to correct this issue, I chose the simplest one:

- For each channel record the neutral, minimum and maximum values
- Determine a range in which the neutral value should fit exactly in the middle of it (neutral-x < neutral < neutral+x, and also min+(max-min)/2=neutral)
    - Determine the delta between the neutral and the lower boundary (delta_low)
    - Determine the delta between the neutral and the upper boundary (delta_high)
    - Keep the smallest delta (delta = min(delta_low, delta_high))
    - Build the range \[neutral-delta : neutral+delta\]
 
Although this method is not optimum because you loose a part of the full range, this is an acceptable method for prototyping the firmware and quickly achieve first results. This could be refined afterwards.  
