import configparser
import socket
import re
import requests
import os


# Setup the Configuration Parser
global config
config = configparser.ConfigParser()
config.sections()
[]
# config.read('config_commands.ini')
# Read config file from main drive where script is located
file_to_open = os.path.join(os.path.abspath(
    os.sep), "\\Automation Controller\\config_commands.ini")
print(file_to_open)
config.read(file_to_open)

global user_Settings
user_Settings = configparser.ConfigParser()
user_Settings.sections()
[]

# Read file from main drive where script is located
file_to_open = os.path.join(os.path.abspath(
    os.sep), "\\Automation Controller\\user_settings.ini")
print(file_to_open)
user_Settings.read(file_to_open)

global hex_command
global read_settings
global bytes_message
global comm_port

# total_theaters = user_Settings['DEFAULT']['total_theaters']
total_theaters = 10


class comm_functions:

    def calculate_cks(msg):
        crc = sum(msg) % 256
        # calc = 0
        # for b in msg:
        #     calc += b
        # res = bytes(calc)
        return crc.to_bytes(1, 'big')

    def rejoined(src, sep='-', _split=re.compile('..').findall):
        return sep.join(_split(src))

    def projector_on(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['power_on']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def projector_off(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['power_off']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def projector_on(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['power_on']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        # RESPONSE DATA: data.startswith(b'\x23\x2f\x00\xc0\x02'):

        return

    def projector_off(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['power_off']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        # RESPONSE DATA: data.startswith(b'\x23\x2f\x00\xc0\x02'):

        return

    def dowser_close(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['dowser_close']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        # RESPONSE DATA: data.startswith(b'\x23\x2f\x00\xc0\x02'):

        return

    def projector_power_state_request():
        response_data = []
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        Power_Status = "Unknown"
        theater_num = 1
        total_theaters = user_Settings['DEFAULT']['total_theaters']
        # while theater_num <= int(total_theaters):
        while theater_num <= int(total_theaters):
            theater = "THEATER_" + str(theater_num)
            theater = str(theater)
            comm_ip = user_Settings[theater]['projector_ip']
            projector_model = user_Settings[theater]['projector_model']
            command_to_execute = config[projector_model]['power_status']
            # print("Command:" + str(command_to_execute))
            comm_port = config[projector_model]['comm_port']
            comm_port = int(comm_port)

            command_to_execute = command_to_execute.encode(
                'utf-8').decode("unicode_escape").encode('latin-1')
            command_to_execute = command_to_execute + \
                comm_functions.calculate_cks(command_to_execute)
            # print(f' Message: {command_to_execute}')
            response = comm_functions.send_packet_with_response(
                comm_ip, comm_port, command_to_execute)
            # print(f'Response: {data_hex_str}')

            if response[0:20] == "20:85:00:c0:10:00:00":
                status_code = response[22:23]
                # print(status_code)

                # Power_Status
                if int(status_code) == 0:
                    Power_Status = 'off'
                elif int(status_code) == 1:
                    Power_Status = 'on'
                else:
                    Power_Status = 'Unknown'

                # print(f'Power_Status: {Power_Status}')
                print("Theater: " + str(theater_num) +
                      " Power is " + Power_Status)

            elif response == "time_out":
                Power_Status = 'Unknown'
                print("Theater: " + str(theater_num) +
                      " Power is " + Power_Status)
            else:
                # print('Error Reading Response String')
                Power_Status = 'Unknown'

            # ADD THEATER NUMBER AND RESPONSE CODE TO
            response_data.append(
                {"theater_num": theater_num, "power_status": Power_Status})

            # INCREMENT THEATER NUMBER FOR THE LOOP
            theater_num += 1
        return response_data

    def lamp_request():
        response_data = []
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')

        theater_num = 1
        total_theaters = user_Settings['DEFAULT']['total_theaters']
        # while theater_num <= int(total_theaters):
        while theater_num <= int(total_theaters):
            theater = "THEATER_" + str(theater_num)
            theater = str(theater)
            comm_ip = user_Settings[theater]['projector_ip']
            projector_model = user_Settings[theater]['projector_model']
            command_to_execute = config[projector_model]['lamp_mode']
            comm_port = config[projector_model]['comm_port']
            comm_port = int(comm_port)

            command_to_execute = command_to_execute.encode(
                'utf-8').decode("unicode_escape").encode('utf-8')
            command_to_execute = command_to_execute + \
                comm_functions.calculate_cks(command_to_execute)

            response = comm_functions.send_packet_with_response(
                comm_ip, comm_port, command_to_execute)

            # print(response[0:17])
            if response[0:17] == "23:2f:00:c0:02:11":
                lcm = response[19:20]
                lamp_state = "Unknown"
                if int(lcm) == 0:
                    Lamp_Control_Mode = 'Status: Lamp is in Standard Mode'
                    lamp_state = "none"
                elif int(lcm) == 1:
                    Lamp_Control_Mode = 'Status: Lamp is On'
                    lamp_state = "on"
                elif int(lcm) == 2:
                    Lamp_Control_Mode = 'Status: Lamp is Off'
                    lamp_state = "off"
                else:
                    Lamp_Control_Mode = 'Unknown'
                    lamp_state = "Unknown"
                print(f'{"Theater " + str(theater_num) + " " + Lamp_Control_Mode}')
            elif response == "time_out":
                print(f'{"Theater " + str(theater_num) + " RESPONSE TIMEOUT"}')
                lamp_state = "Unknown"
            else:
                # print('Error Reading Response String')
                lcm = "unknown"
                lamp_state = "Unknown"

            # ADD THEATER NUMBER AND RESPONSE CODE TO
            response_data.append(
                {"theater_num": theater_num, "bulb_state": lamp_state})

            # INCREMENT THEATER NUMBER FOR THE LOOP
            theater_num += 1
        return response_data

    def dowser_open(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['dowser_open']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        # RESPONSE DATA: data.startswith(b'\x23\x2f\x00\xc0\x02'):

        return

    def lamp_on(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['lamp_on']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def lamp_off(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['lamp_off']
        comm_port = config[projector_model]['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('utf-8')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        # RESPONSE DATA: data.startswith(b'\x23\x2f\x00\xc0\x02'):

        return

    def ecna_exe(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['ecna_ip']
        comm_port = config['ECNA_FIVE']['ecna_comm_port']
        comm_port = int(comm_port)
        command_to_execute = config['ECNA_FIVE']['ecna_mac_event_13']

        print(f' HOST: {comm_ip}:{comm_port}')
        print(f' RAW COMMAND: {command_to_execute}')

        command_to_execute = command_to_execute.encode('ascii')
        command_to_execute = command_to_execute + \
            comm_functions.calculate_cks(command_to_execute)

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        print("ECNA Theater " + theater_num + "Executed")
        return

    def sound_processor(theater_num, exe_command):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['sound_device_ip']
        model = user_Settings[theater]['sound_processor_model']
        if exe_command == "movie":
            command_to_execute = config[model]['format_movie']
        elif exe_command == "non_sync":
            command_to_execute = config[model]['format_non_sync']

        comm_port = config[model]['comm_port']
        comm_port = int(comm_port)

        print(f' HOST: {comm_ip}:{comm_port}')
        print(f' RAW COMMAND: {command_to_execute}')

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('ascii')

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)
        return

    def server_shutdown(theater_num):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['server_ip']
        command_to_execute = config['GDC_NETSOCKET']['command_shutdown']
        comm_port = config['GDC_NETSOCKET']['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('ascii')

        print(f' HOST: {comm_ip}:{comm_port}')
        print(f' RAW COMMAND: {command_to_execute}')

        # comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def server_automation(theater_num, action_state):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['server_ip']

        if action_state == "pause_film":
            command_to_execute = config['GDC_NETSOCKET']['command_pause']
        elif action_state == "restore_film":
            command_to_execute = config['GDC_NETSOCKET']['command_restore']
        elif action_state == "play_film":
            command_to_execute = config['GDC_NETSOCKET']['command_play']

        comm_port = config['GDC_NETSOCKET']['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('ascii')

        print(f' HOST: {comm_ip}:{comm_port}')
        print(f' RAW COMMAND: {command_to_execute}')

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def all_bulb_on():
        theater_num = 1
        total_theaters = user_Settings['DEFAULT']['total_theaters']
        # while theater_num <= int(total_theaters):
        while theater_num <= int(total_theaters):
            # Send Projection Lamp On Command
            comm_functions.lamp_on(str(theater_num))
            print(f' Theater {theater_num} Lamp On Executed')
            theater_num += 1
        return

    def all_bulb_off():
        theater_num = 1
        total_theaters = user_Settings['DEFAULT']['total_theaters']
        # while theater_num <= int(total_theaters):
        while theater_num <= int(total_theaters):
            # Send Projection Lamp On Command
            comm_functions.lamp_off(str(theater_num))
            print(f' Theater {theater_num} Lamp Off Executed')
            theater_num += 1
        return

    def all_functions(action_state):
        theater_num = 1
        total_theaters = user_Settings['DEFAULT']['total_theaters']
        # while theater_num <= int(total_theaters):
        while theater_num <= int(total_theaters):
            # Send Server Command
            comm_functions.server_automation(str(theater_num), action_state)

            if action_state != "restore_film":
                # Send Projection Lamp On Command
                comm_functions.lamp_on(str(theater_num))

            print(f' Theater {theater_num} Executed')
            theater_num += 1
        return

    def send_packet(comm_ip, comm_port, command_to_execute):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((comm_ip, comm_port))
            print(f' COMMAND ENCODED: {command_to_execute}')
            s.send(command_to_execute)
        except socket.timeout:
            print('Connection Failed. No data sent.')
            # messagebox.showinfo("Message", "Connection Failed. No data sent.")

        s.close()

        return

    def send_packet_with_response(comm_ip, comm_port, command_to_execute):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((comm_ip, comm_port))
            # print(f' COMMAND ENCODED: {command_to_execute}')
            s.send(command_to_execute)
        except socket.timeout:
            print('Connection Failed. No data sent.')
            # messagebox.showinfo("Message", "Connection Failed. No data sent.")
        try:
            data = s.recv(4096)
            # print(f' Response Recieved: {data}')
            # messagebox.showinfo("Message", "Command Pause Executed.")
            data_hex_str = comm_functions.rejoined(data.hex(), sep=':')
            # print(f' Response: {data_hex_str}')
        except socket.timeout:
            # print('No Response. Data Received Time Out.')
            data_hex_str = "time_out"
            # messagebox.showinfo("Message", "Unable to communicate to projector. Time Out.")
        s.close()

        return data_hex_str

    def ProjPowerStatus():
        response_data = []
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')

        theater_num = 8
        theater = "THEATER_" + str(theater_num)
        theater = str(theater)
        projector_ip = user_Settings[theater]['projector_ip']
        projector_model = user_Settings[theater]['projector_model']
        command_to_execute = config[projector_model]['power_status']
        comm_port = config[projector_model]['comm_port']
        network_port = int(comm_port)

        # projector_ip: str = '10.216.108.191'
        # network_port: int = 43728
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((projector_ip, network_port))
        print(f'Connected to {projector_ip}:{network_port}')
        # message = b'\x00\x85\x00\x00\x01\x01\x87'
        print(f'command_to_execute: {command_to_execute}')

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('latin-1')

        print(f'Command to Execute Encoded: {command_to_execute}')

        message = b'\x00\x85\x00\x00\x01\x01\x87'
        print(f'Message: {message}')
        message_hex_str = comm_functions.rejoined(message.hex(), sep=':')
        print(f'Message hex: {message_hex_str}')
        s.send(message)

        try:
            data = s.recv(4096)
            data_hex_str = comm_functions.rejoined(data.hex(), sep=':')
            print(f'Response: {data_hex_str}')

            # External_Control_Status
            if data[6] == 0:
                External_Control_Status = 'Off'
            elif data[6] == 1:
                External_Control_Status = 'On'
            else:
                External_Control_Status = 'Unknown'
            print(f'External_Control_Status: {External_Control_Status}')

            # Power_Status
            if data[7] == 0:
                Power_Status = 'Off'
            elif data[7] == 1:
                Power_Status = 'On'
            else:
                Power_Status = 'Unknown'
            print(f'Power_Status: {Power_Status}')

            # Lamp Cooling Processing
            if data[8] == 0:
                Lamp_Cooling_Processing = 'No execution'
            elif data[8] == 1:
                Lamp_Cooling_Processing = 'During execution'
            else:
                Lamp_Cooling_Processing = 'Unknown'
            print(f'Lamp_Cooling_Processing: {Lamp_Cooling_Processing}')

            # On/Off Processing
            if data[9] == 0:
                On_Off_Processing = 'No execution'
            elif data[9] == 1:
                On_Off_Processing = 'During execution'
            else:
                On_Off_Processing = 'Unknown'
            print(f'On_Off_Processing: {On_Off_Processing}')

            # Projector Process Status
            if data[10] == 0:
                Projector_Process_Status = 'Standby'
            elif data[10] == 1:
                Projector_Process_Status = 'Power On Protect (before Lamp(Light) control)'
            elif data[10] == 2:
                Projector_Process_Status = 'Ignition'
            elif data[10] == 3:
                Projector_Process_Status = 'Power On Running'
            elif data[10] == 4:
                Projector_Process_Status = 'Running (Power On / Lamp(Light) On)'
            elif data[10] == 5:
                Projector_Process_Status = 'Cooling'
            # b'06' Reserved
            elif data[10] == 7:
                Projector_Process_Status = 'Reset Wait'
            elif data[10] == 8:
                Projector_Process_Status = 'Fan Stop Error (before Cooling)'
            elif data[10] == 9:
                Projector_Process_Status = 'Lamp Retry'
            elif data[10] == 10:
                Projector_Process_Status = 'Lamp(Light) Error (before Cooling)'
            elif data[10] == 12:
                Projector_Process_Status = 'Running (Power On / Lamp(Light) Off)'
            else:
                On_Off_Processing = 'Unknown'
            print(f'Projector_Process_Status: {Projector_Process_Status}')

            # Store Processing
            if data[13] == 0:
                Store_Processing = 'No execution'
            elif data[13] == 1:
                Store_Processing = 'During execution'
            else:
                Store_Processing = 'Unknown'
            print(f'Store_Processing: {Store_Processing}')

            # Lamp Status
            if data[14] == 0:
                Lamp_Status = 'Lamp(Light) Off'
            elif data[14] == 1:
                Lamp_Status = 'Lamp(Light) On,  Dual-Lamp: Lamp1 On/Lamp2 Off'
            elif data[14] == 2:
                Lamp_Status = 'Lamp1 Off/Lamp2 On'
            elif data[14] == 3:
                Lamp_Status = 'Lamp1and2 On'
            else:
                Lamp_Status = 'Unknown'
            print(f'Lamp_Status: {Lamp_Status}')

            # Processing of Lamp
            if data[15] == 0:
                Processing_of_Lamp = 'No execution'
            elif data[15] == 1:
                Processing_of_Lamp = 'During execution'
            else:
                Processing_of_Lamp = 'Unknown'
            print(f'Processing_of_Lamp: {Processing_of_Lamp}')

            # Lamp Mode Setting (NC900C-A and NC1000C)
            if data[16] == 0:
                Lamp_Mode_Setting = 'Dual'
            elif data[16] == 1:
                Lamp_Mode_Setting = 'Lamp1'
            elif data[16] == 2:
                Lamp_Mode_Setting = 'Lamp2'
            else:
                Lamp_Mode_Setting = 'Unknown'
            print(
                f'Lamp_Mode_Setting: {Lamp_Mode_Setting}  (NC900C-A and NC1000C)')

            # Cooling Remaining Time(in sec)
            b_low = data[17]
            b_high = data[18]
            Cooling_Remaining_Time = int.from_bytes(
                bytes([b_high, b_low]), 'little')
            print(f'Cooling_Remaining_Time: {Cooling_Remaining_Time} seconds')

            # Remaining Time of Lamp
            b_low = data[19]
            b_high = data[20]
            Remaining_Time_of_Lamp = int.from_bytes(
                bytes([b_high, b_low]), 'big')
            print(
                f'Remaining_Time_of_Lamp: {Remaining_Time_of_Lamp} hours (NC900C and NC1000C')

        except socket.timeout:
            pass
        s.close()
        return
