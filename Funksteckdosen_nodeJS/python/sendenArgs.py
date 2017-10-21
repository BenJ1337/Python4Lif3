import Transmitter
import sys
import time

if __name__ == "__main__":
	args = sys.argv
	transmit = Transmitter.TransmitterS()
	transmit.transmit_code( args[1]  )
	print( args[1]  ) 