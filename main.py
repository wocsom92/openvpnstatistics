from openVpnParser import OpenVpnParser
from connections_db import ConnectionDB
from user import User
from config import Config
from web_generator import WebGenerator
import time
import threading

def ip_retriever():
    while True:
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_ip_table()
        connectionDb.update_missing_connections()
        time.sleep(Config.ip_update_interval)

def db_clean():
    while True:
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.remove_old_connections()
        connectionDb.vacuum()
        time.sleep(Config.db_clean_interval)

def output_txt_file_generator():
    while True:
        connectionDb = ConnectionDB(Config.db_file_mame)
        users = connectionDb.select_distinct_common_names()
        with open(Config.output_file_name, 'w') as file:
            pass
        for user in users:
            lastSeen = connectionDb.select_last_seen(user)
            inBytesToday, outBytesToday = connectionDb.select_sum_bytes_for_current_day(user)
            inBytesWeek, outBytesWeek = connectionDb.select_sum_bytes_for_last_week(user)
            inBytesMonth, outBytesMonth = connectionDb.select_sum_bytes_for_last_month(user)
            formatedUser = User(user, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth, lastSeen, '')
            with open(Config.output_file_name, 'a') as file:
                file.write( formatedUser.print_info() + '\n')
            
        time.sleep(Config.output_file_write_interval)

def output_web_file_generator():
    while True:
        webGenerator = WebGenerator( Config.web_file_path )
        webGenerator.generate()
        time.sleep(Config.output_file_write_interval)

def file_parse():
    while True:
        parser = OpenVpnParser()
        data = parser.parseOpenVpnStatus(Config.input_file_name)    
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_connection_table()
        for connection in data:
            existing = connectionDb.select_connection(connection.common_name, connection.connected_since)
            if existing: 
                connectionDb.update_connection(connection)
            else:
                connectionDb.insert_connection(connection)
        time.sleep(Config.input_file_parse_interval)

def main():
    output__txt_file_generator_thread = threading.Thread(target=output_txt_file_generator)
    output__txt_file_generator_thread.daemon = True
    output__txt_file_generator_thread.start()

    output__web_file_generator_thread = threading.Thread(target=output_web_file_generator)
    output__web_file_generator_thread.daemon = True
    output__web_file_generator_thread.start()

    dbclean_thread = threading.Thread(target=db_clean)
    dbclean_thread.daemon = True
    dbclean_thread.start()

    ip_retriever_thread = threading.Thread(target=ip_retriever)
    ip_retriever_thread.daemon = True
    ip_retriever_thread.start()

    file_parser_thread = threading.Thread(target=file_parse)
    file_parser_thread.daemon = True
    file_parser_thread.start()

    while True:
        pass
    
if __name__ == "__main__":
    main()