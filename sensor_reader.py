MIN_SUB_BIT_PER_BIT = 24
HEADER_LENGTH_IN_BITS = 10
MSG_LENGTH_IN_BITS = 32

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

    print(bit_buffer)
    bit_buffer += "00"
    if(len(bit_buffer) == MSG_LENGTH_IN_BITS):
        print("Sensor ID: " +
              str(int(bit_buffer[0:8], 2)) + " - " + str(int(bit_buffer[8:24], 2)))
    else:
        print("----")


with open("test/car_sensor_data.txt") as fileobj:
    for line in fileobj:
        for current_bit in line:
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
