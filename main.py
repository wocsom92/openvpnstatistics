from openVpnParser import OpenVpnParser
from connections_db import ConnectionDB
from connection import Connection
from user import User
import time
import threading

def output_generator():
    while True:
        connectionDb = ConnectionDB()
        users = connectionDb.select_distinct_common_names()
        with open('data.txt', 'w') as file:#add header 
            pass
        for user in users:
            lastSeen = connectionDb.select_last_seen(user)
            inBytesToday, outBytesToday = connectionDb.select_sum_bytes_for_current_day(user)
            inBytesWeek, outBytesWeek = connectionDb.select_sum_bytes_for_last_week(user)
            inBytesMonth, outBytesMonth = connectionDb.select_sum_bytes_for_last_month(user)
            formatedUser = User(user, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth, lastSeen, '')
            with open('data.txt', 'a') as file:
                file.write( formatedUser.print_info() + '\n')
            
        time.sleep(23)

def main():
    second_thread = threading.Thread(target=output_generator)
    second_thread.daemon = True  # Set as daemon thread to automatically exit when main thread exits
    second_thread.start()

    while True: 
        parser = OpenVpnParser()
        data = parser.parseOpenVpnStatus('/var/log/openvpn/status.log')
        #data = parser.parseOpenVpnStatus('data/status.log')    
        connectionDb = ConnectionDB()
        connectionDb.create_connection_database()
        for connection in data:
            existing = connectionDb.select_connection(connection.common_name, connection.connected_since)
            if existing: 
                connectionDb.update_connection(connection)
            else:
                connectionDb.insert_connection(connection)
        time.sleep(14)
    
if __name__ == "__main__":
    main()