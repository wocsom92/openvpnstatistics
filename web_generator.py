from connections_db import ConnectionDB
from config import Config
from datetime import datetime, timedelta
import os

class WebGenerator:
    def __init__(self, file_name ):
        self.file_name = file_name 
    
    def generate(self):
        connectionDb = ConnectionDB( Config.db_file_mame )
        users = connectionDb.select_distinct_common_names()
        with open(Config.web_file_path, 'w') as file:
            pass
        with open(Config.web_file_path, 'a') as file:
                file.write( self.html_part1() )
        for user in users:
            lastSeen = connectionDb.select_last_seen(user)
            inBytesToday, outBytesToday = connectionDb.select_sum_bytes_for_current_day(user)
            inBytesWeek, outBytesWeek = connectionDb.select_sum_bytes_for_last_week(user)
            inBytesMonth, outBytesMonth = connectionDb.select_sum_bytes_for_last_month(user)
            with open(Config.web_file_path, 'a') as file:
                file.write(  self.html_card(user, lastSeen, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth) )
        
        with open(Config.web_file_path, 'a') as file:
                file.write( self.html_last_part() )

    def html_part1(self):
         return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1f1f1f;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }

        .container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
        }

        .user-card,
        .location-card {
            background-color: #333333;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            margin: 10px;
            padding: 20px;
            width: calc(25% - 40px); /* 4 users per row */
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .user-card:hover,
        .location-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        }

        .status-icon {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 5px;
        }

        .online {
            background-color: green;
        }

        .offline {
            background-color: red;
        }

        .away {
            background-color: orange;
        }

        .long-time-off {
            background-color: gray;
        }

        h2 {
            font-size: 20px;
            margin-top: 0;
            color: #3498db;
        }

        .traffic-data {
            margin-top: 20px;
            font-size: 14px;
            color: #aaaaaa;
        }

        .traffic-label {
            font-weight: bold;
            color: #dddddd;
        }

        /* Responsive adjustments */
        @media screen and (max-width: 768px) {
            .user-card {
                width: 100%; /* 1 user per row */
            }
            .last-refreshed {
                width: 100%; /* 1 user per row */
            }
            .location-card {
                width: 100%; /* 1 user per row */
            }
        }

        @media screen and (max-width: 480px) {
            .user-card {
                width: 100%; /* 1 user per row */
            }
            .last-refreshed {
                width: 100%; /* 1 user per row */
            }
            .location-card {
                width: 100%; /* 1 user per row */
            }
        }

        .last-refreshed {
            background-color: #333333;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            margin: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .last-refreshed:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        }

        .last-refreshed span {
            font-weight: bold;
            color: #dddddd;
        }
        .location-card h2 {
            font-size: 24px;
            color: #e74c3c; /* Red color for the header */
            margin-bottom: 10px;
        }

        .location-data ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .location-data li {
            font-size: 14px;
            color: #aaaaaa;
            margin-bottom: 10px; /* Increased spacing between list items */
            padding-left: 15px; /* Left padding for better separation */
            position: relative;
        }

        .location-data li strong {
            color: #ffffff; /* White color for strong elements */
        }

        .location-data li::before {
            content: "▹"; /* Using a bullet symbol for better visual separation */
            color: #3498db; /* Blue color for the bullet symbol */
            font-size: 10px;
            position: absolute;
            left: 0;
        }

        .location-group {
            margin-top: 15px;
            border-top: 1px solid #aaaaaa;
            padding-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
'''

    def html_last_part(self):
         current_time = datetime.now()
         formatted_time = current_time.strftime("%B %d %H:%M")

         folder_name = Config.db_file_location
         file_name = Config.db_file_mame + '.db'
         file_path = os.path.join(folder_name, file_name)
         db_size = 0

         if os.path.exists(file_path):
            db_size = os.path.getsize(file_path)
        
         connectionDb = ConnectionDB( Config.db_file_mame )
         ipCount = connectionDb.ipCount()
         sys_resources = connectionDb.select_last_system_resources()
         if sys_resources == None:
             retVal = '''
         <div class="last-refreshed">
            <p>Last Refreshed: <span>''' + formatted_time + '''</span></p>
            <p>Database size: <span>''' + self.formatBytes(db_size) + '''</span></p>
            <p>Distinct Ips: <span>''' + str(ipCount[0]) + '''</span></p>
        </div>'''
         else:
            retVal = '''
         <div class="last-refreshed">
            <p>Last Refreshed: <span>''' + formatted_time + '''</span></p>
            <p>Database size: <span>''' + self.formatBytes(db_size) + '''</span></p>
            <p>Distinct Ips: <span>''' + str(ipCount[0]) + '''</span></p>
            <p>Disk: <span>''' + str(sys_resources[1]) + ''' %</span></p>
            <p>RAM: <span>''' + str(sys_resources[2]) + ''' %</span></p>
            <p>Processes: <span>''' + str(sys_resources[6]) + '''</span></p>
            <p>Load Average 1m: <span>''' + str(sys_resources[3])  + '''</span></p>
            <p>Load Average 5m: <span>''' + str(sys_resources[4])  + '''</span></p>
            <p>Load Average 15m: <span>''' + str(sys_resources[5])  + '''</span></p>
        </div>'''
         retVal = retVal + self.html_location_card()
         retVal = retVal +'''</div>
</body>
</html>
'''
         return retVal

    def html_card(self, username, last_seen, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth ):
        current_time = datetime.now()
        last_seen_data = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
        time_difference = current_time - last_seen_data

        online_threshold = timedelta(minutes=10)
        away_treshold = timedelta(hours=1)
        offline_treshold = timedelta(hours=24)
# Check if Last Seen time is within the threshold
        if time_difference <= online_threshold:
            status = 'online'
        else:
            if time_difference < away_treshold:
                status = 'away'
            else:
                if time_difference < offline_treshold:
                    status = 'offline'
                else:
                    status = 'long-time-off'
        if Config.enable_full_user_name_in_web == True:
            card_text = '''
            <div class="user-card">
                <h2>''' + str( username )  + ''' <span class="status-icon '''+ status + '''"></span> ''' + '''</h2>

                <div class="traffic-data">
                    <p class="traffic-label">Daily  Usage: ''' + self.formatBytes( inBytesToday ) + '''</p>
                    <p class="traffic-label">Weekly Usage: ''' + self.formatBytes( inBytesWeek ) + '''</p>
                    <p class="traffic-label">Monthly Usage: ''' + self.formatBytes( inBytesMonth )  + '''</p>
                </div>
            </div>'''
        else:
            card_text = '''
            <div class="user-card">
                <h2>''' + str( username[0] )  + ''' <span class="status-icon '''+ status + '''"></span> ''' + '''</h2>

                <div class="traffic-data">
                    <p class="traffic-label">Daily  Usage: ''' + self.formatBytes( inBytesToday ) + '''</p>
                    <p class="traffic-label">Weekly Usage: ''' + self.formatBytes( inBytesWeek ) + '''</p>
                    <p class="traffic-label">Monthly Usage: ''' + self.formatBytes( inBytesMonth )  + '''</p>
                </div>
            </div>'''
         
        return card_text
    
    def formatBytes(self, bytes):
        if(bytes < 1024):
            return f"{bytes:4.0f}" + "  B"
        if( bytes < 1024*1024):
            return  f"{bytes/1024:4.0f}"+ " kB"
        if( bytes < 1024*1024*1024):
            return  f"{bytes/1024/1024:4.0f}" + " MB"
        if( bytes < 1024*1024*1024*1024):
            return  f"{bytes/1024/1024/1024:4.2f}" + " GB"
        if( bytes < 1024*1024*1024*1024*1024):
            return  f"{bytes/1024/1024/1024/1024:4.2f}" + " TB"
        else:
            return f"{bytes:5.0f}" + "  B"
        
    def html_location_card(self):
        connectionDb = ConnectionDB( Config.db_file_mame )
        locations = connectionDb.selectLocations()
        retVal = '''
        <!-- Location Card -->
        <div class="location-card">
            <h2>Location Information</h2>
            <div class="location-data">
        '''
        for location in locations:
            if Config.enable_provider_in_web == True:
                retVal += '''
                    <div class="location-group">
                        <ul>
                            <li><strong>City: </strong>''' + location[2]+ '''</li>
                            <li><strong>Region: </strong>''' + location[1] + '''</li>
                            <li><strong>Country: </strong>''' + location[0]+ '''</li>
                            <li><strong>Provider: </strong> <br>''' + location[3]+ '''</li>
                        </ul>
                    </div>
                '''
            else:
                retVal += '''
                    <div class="location-group">
                        <ul>
                            <li><strong>City: </strong>''' + location[2]+ '''</li>
                            <li><strong>Region: </strong>''' + location[1] + '''</li>
                            <li><strong>Country: </strong>''' + location[0]+ '''</li>
                        </ul>
                    </div>
                '''
        retVal += '''          
            </div>
        </div>
        '''
        return retVal