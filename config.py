class Config:
        input_file_parse_interval = 14
        input_file_name = '/var/log/openvpn/status.log'
        db_file_mame = 'connection'
        output_file_name = 'data.txt'
        output_file_write_interval = 69
        db_clean_interval = 60 * 60 * 24 #once per day
        db_clean_how_many_days_keep_data = 31
        ip_update_interval = 3600 #once per hour
        web_file_path = '/var/www/html/vpn/vpn.html'
        enable_provider_in_web = True
        enable_full_user_name_in_web = True
        ip_information_shown_in_web = 7 #in days

        def test():
                Config.input_file_parse_interval = 14
                Config.input_file_name = 'data/status.log'
                Config.db_file_mame = 'connection'
                Config.output_file_name = 'data.txt'
                Config.output_file_write_interval = 69
                Config.db_clean_interval = 60 * 60 * 24 #once per day
                Config.db_clean_how_many_days_keep_data = 31
                Config.ip_update_interval = 10
                Config.web_file_path = 'data/vpn.html'
                Config.enable_provider_in_web = False
                Config.enable_full_user_name_in_web = True
                Config.ip_information_shown_in_web = 31
        
        def production():
                Config.input_file_parse_interval = 14
                Config.input_file_name = '/var/log/openvpn/status.log'
                Config.db_file_mame = 'connection'
                Config.output_file_name = 'data.txt'
                Config.output_file_write_interval = 69
                Config.db_clean_interval = 60 * 60 * 24 #once per day
                Config.db_clean_how_many_days_keep_data = 31
                Config.ip_update_interval = 3600 #once per hour
                Config.web_file_path = '/var/www/html/vpn/vpn.html'
                Config.enable_provider_in_web = False
                Config.enable_full_user_name_in_web = False
                Config.ip_information_shown_in_web = 7