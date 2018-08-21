import RPi.GPIO as GPIO

MIN_SUB_BIT_PER_BIT = 18
HEADER_LENGTH_IN_BITS = 10
MSG_LENGTH_IN_BITS = 36
SENSOR_IDS = ["8", "11"]

# Setup GPIO Input
INPUT_PIN = 23
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_PIN, GPIO.IN)

temp_bit_buffer = ""
msg_buffer = ""
parsing_state = "looking_for_header"
previous_bit = ""


def parse_msg(msg_buffer):
    temp_parsing_buffer = ""
    bit_buffer = ""
    previous_bit = ""

    for current_bit in msg_buffer:
        if(previous_bit != "" and previous_bit != current_bit):
            num_bits = int(len(temp_parsing_buffer)/MIN_SUB_BIT_PER_BIT)
            if(num_bits == 0):
                bit_buffer += previous_bit
            for _ in range(num_bits):
                bit_buffer += previous_bit
            temp_parsing_buffer = ""
        else:
            temp_parsing_buffer += current_bit
        previous_bit = current_bit

    if(temp_parsing_buffer != ""):
        num_bits = int(len(temp_parsing_buffer)/MIN_SUB_BIT_PER_BIT)
        if(num_bits == 0):
            bit_buffer += previous_bit

        for _ in range(num_bits):
            bit_buffer += previous_bit
        temp_parsing_buffer = ""

    
    if(len(bit_buffer) >= 16):
	print(bit_buffer)
	sensor_id = str(int(bit_buffer[0:4], 2))
	if(sensor_id in SENSOR_IDS):
        	print("Sensor ID: " + sensor_id + " - " + str(int(bit_buffer[4:10], 2)) + " | " + str(int(bit_buffer[4:12], 2)) + " | " + str(int(bit_buffer[6:14], 2)) + " | " + str(int(bit_buffer[8:16], 2)) + " | 0x" + bit_buffer[12:])
    	else:
		print("######### Unknown Sensor ID: " + sensor_id)
    else:
        print("----")


while True:
    current_bit = str(GPIO.input(INPUT_PIN)).strip()
    if(parsing_state == "looking_for_header"):
        if(previous_bit == "0" and current_bit == "1" and len(temp_bit_buffer)/MIN_SUB_BIT_PER_BIT >= HEADER_LENGTH_IN_BITS):
            parsing_state = "reading_msg"
            temp_bit_buffer = ""
            msg_buffer += current_bit
        else:
            temp_bit_buffer += current_bit

    elif(parsing_state == "reading_msg"):
        if(len(msg_buffer)/MIN_SUB_BIT_PER_BIT >= MSG_LENGTH_IN_BITS):
            parsing_state = "parsing_msg"
        else:
            msg_buffer += current_bit

    if(parsing_state == "parsing_msg"):
        parse_msg(msg_buffer)
        msg_buffer = ""
        temp_bit_buffer = ""
        parsing_state = "looking_for_header"
        previous_bit = ""
    else:
        previous_bit = current_bit
