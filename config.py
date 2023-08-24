class Config:
        input_file_parse_interval = 14
        input_file_mame = '/var/log/openvpn/status.log'
        db_file_mame = 'connection'
        output_file_name = 'data.txt'
        output_file_write_interval = 69
        db_clean_interval = 60 * 60 * 24 #once per day
        db_clean_how_many_days_keep_data = 31
        ip_update_interval = 3600 #once per hour
        web_file_path = '/var/www/html/vpn/vpn.html'