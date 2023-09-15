class Config:
        #input file parsing
        input_file_parse_interval = 14
        input_file_name = '/var/log/openvpn/status.log'
        #output file settings
        db_file_mame = 'connection'
        db_file_location = 'data'
        output_file_write_interval = 69
        #db clean functionality
        db_clean_interval = 60 * 60 * 24 #once per day
        db_clean_how_many_days_keep_data = 31
        #ip retrieving
        location_info = True
        ip_update_interval = 3600 #once per hour
        #html outputfile
        web_file_path = '/var/www/html/vpn/vpn.html'
        enable_provider_in_web = True
        enable_full_user_name_in_web = True
        ip_information_shown_in_web = 7 #in days
        #system monitoring
        sys_update_interval = 3600
        disk_to_monitor = '/'

        def test():
                Config.input_file_parse_interval = 14
                Config.input_file_name = 'data/status.log'
                Config.db_file_mame = 'connection'
                Config.db_file_location = 'data'
                Config.output_file_write_interval = 10
                Config.db_clean_interval = 60 * 60 * 24 
                Config.db_clean_how_many_days_keep_data = 31
                Config.ip_update_interval = 10
                Config.web_file_path = 'data/vpn.html'
                Config.enable_provider_in_web = False
                Config.enable_full_user_name_in_web = True
                Config.ip_information_shown_in_web = 31
                Config.sys_update_interval = 15
                Config.disk_to_monitor = '/dev/disk1s5'
                Config.location_info = False
        
        def production():
                Config.input_file_parse_interval = 14
                Config.input_file_name = '/var/log/openvpn/status.log'
                Config.db_file_mame = 'connection'
                Config.db_file_location = '/shared_data'
                Config.output_file_write_interval = 69
                Config.db_clean_interval = 60 * 60 * 24
                Config.db_clean_how_many_days_keep_data = 31
                Config.ip_update_interval = 60 
                Config.web_file_path = '/var/www/html/vpn/vpn.html'
                Config.enable_provider_in_web = False
                Config.enable_full_user_name_in_web = True
                Config.ip_information_shown_in_web = 7
                Config.sys_update_interval = 600
                Config.disk_to_monitor = '/'
                Config.location_info = False