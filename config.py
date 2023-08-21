class Config:
        inputFileParseInterval = 14
        inputFileName = '/var/log/openvpn/status.log'
        #inputFileName = 'data/status.log'
        dbFileName = 'connection'
        outputFileName = 'data.txt'
        outputFileWriteInterval = 23
        db_clean_interval = 60 * 60 * 24 #once per day
        db_clean_how_many_days_keep_data = 31
        ip_update_interval = 3600 #once per hour