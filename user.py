class User:
    def __init__(self, name, bytes_in_day, bytes_out_day, bytes_week_in, bytes_week_out,
                 bytes_in_month, bytes_out_month, last_seen, online):
        self.name = name
        self.bytes_in_day = bytes_in_day
        self.bytes_out_day = bytes_out_day
        self.bytes_week_in = bytes_week_in
        self.bytes_week_out = bytes_week_out
        self.bytes_in_month = bytes_in_month
        self.bytes_out_month = bytes_out_month
        self.last_seen = last_seen
        self.online = online

    def print_info(self):
        info = f"{self.name:10} "
        info += f"{self.bytes_in_day/1024/1024:10.2f} MB "
        info += f"{self.bytes_out_day/1024/1024:10.2f} MB "
        info += f"{self.bytes_week_in/1024/1024:10.2f} MB "
        info += f"{self.bytes_week_out/1024/1024:10.2f} MB "
        info += f"{self.bytes_in_month/1024/1024:10.2f} MB "
        info += f"{self.bytes_out_month/1024/1024:10.2f} MB "
        info += f"{self.last_seen:15} "
        info += f"{self.online:10}"
        return info