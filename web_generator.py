from connections_db import ConnectionDB
from config import Config

class WebGenerator:
    def __init__(self, file_name ):
        self.file_name = file_name 
    
    def generate(self):
        connectionDb = ConnectionDB( Config.dbFileName )
        users = connectionDb.select_distinct_common_names()
        with open(Config.webFilePath, 'w') as file:
            pass
        with open(Config.webFilePath, 'a') as file:
                file.write( self.html_part1() )
        for user in users:
            lastSeen = connectionDb.select_last_seen(user)
            inBytesToday, outBytesToday = connectionDb.select_sum_bytes_for_current_day(user)
            inBytesWeek, outBytesWeek = connectionDb.select_sum_bytes_for_last_week(user)
            inBytesMonth, outBytesMonth = connectionDb.select_sum_bytes_for_last_month(user)
            with open(Config.webFilePath, 'a') as file:
                file.write(  self.html_card(user, lastSeen, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth) )
        
        with open(Config.webFilePath, 'a') as file:
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

        .user-card {
            background-color: #333333;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            margin: 10px;
            padding: 20px;
            width: calc(25% - 40px); /* 4 users per row */
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .user-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
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
                width: calc(50% - 40px); /* 2 users per row */
            }
        }

        @media screen and (max-width: 480px) {
            .user-card {
                width: 100%; /* 1 user per row */
            }
        }
    </style>
</head>
<body>
    <div class="container">
'''

    def html_last_part(self):
         return '''
</div>
</body>
</html>
'''

    def html_card(self, username, last_seen, inBytesToday, outBytesToday, inBytesWeek, outBytesWeek, inBytesMonth, outBytesMonth ):
        card_text = '''
        <div class="user-card">
            <h2>''' + str( username[0] )  + '''</h2>
            <div class="traffic-data">
                <p class="traffic-label">Daily  Usage: ''' + self.formatBytes( inBytesToday ) + '''</p>
                <p class="traffic-label">Weekly Usage: ''' + self.formatBytes( inBytesWeek ) + '''</p>
                <p class="traffic-label">Monthly Usage: ''' + self.formatBytes( inBytesMonth )  + '''</p>
                <p class="traffic-label">Last Seen: ''' + f"{last_seen[2:-3]:10} "  + '''</p>
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