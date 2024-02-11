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

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def server_automation(theater_num, action_state):
        user_Settings.read('user_settings.ini')
        config.read('config_commands.ini')
        theater_num = theater_num
        theater = "THEATER_" + theater_num
        theater = str(theater)
        comm_ip = user_Settings[theater]['server_ip']

        if action_state == "Pause":
            command_to_execute = config['GDC_NETSOCKET']['command_pause']
        elif action_state == "Restore":
            command_to_execute = config['GDC_NETSOCKET']['command_restore']

        comm_port = config['GDC_NETSOCKET']['comm_port']
        comm_port = int(comm_port)

        command_to_execute = command_to_execute.encode(
            'utf-8').decode("unicode_escape").encode('ascii')

        print(f' HOST: {comm_ip}:{comm_port}')
        print(f' RAW COMMAND: {command_to_execute}')

        comm_functions.send_packet(comm_ip, comm_port, command_to_execute)

        return

    def all_functions(action_state):
        theater_num = 1
        # while theater_num <= int(total_theaters):
        while theater_num <= int(1):
            # Send Server Command
            comm_functions.server_automation(str(theater_num), action_state)

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
        try:
            data = s.recv(4096)
            print(f' Response Recieved: {data}')
            # messagebox.showinfo("Message", "Command Pause Executed.")
            data_hex_str = comm_functions.rejoined(data.hex(), sep=':')
            print(f' Response: {data_hex_str}')
        except socket.timeout:
            print('No Response. Data Received Time Out.')
            # messagebox.showinfo("Message", "Unable to communicate to projector. Time Out.")
        s.close()

        return
