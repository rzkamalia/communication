from configparser import ConfigParser
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) > 1:
    argv_input_cfg = str(sys.argv[1])
    filename_config = os.path.join(BASE_DIR, 'config/config_' + argv_input_cfg + '.cfg')

config_object = ConfigParser()

config_object.read(filename_config)
config_input = config_object['INPUT']
source_input = config_input['source_input']
stream_name = '/' + config_input['stream_name']
port_artis = int(config_input['port_artis'])