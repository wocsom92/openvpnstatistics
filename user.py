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
        info = f"{self.name:6} "
        info += self.formatBytes( self.bytes_in_day ) + " "
        info += self.formatBytes( self.bytes_out_day ) + " "
        info += self.formatBytes( self.bytes_week_in ) + " "
        info += self.formatBytes( self.bytes_week_out ) + " "
        info += self.formatBytes( self.bytes_in_month ) + " "
        info += self.formatBytes( self.bytes_out_month ) + " "
        info += f"{self.last_seen:15} "
        return info
    
    def formatBytes(self, bytes):
        if(bytes < 1024):
            return f"{bytes:4.0f}" + "  B"
        if( bytes < 1024*1024):
            return  f"{bytes/1024:4.0f}"+ " kB"
        if( bytes < 1024*1024*1024):
            return  f"{bytes/1024/1024:4.0f}" + " MB"
        if( bytes < 1024*1024*1024*1024):
            return  f"{bytes/1024/1024/1024:4.0f}" + " GB"
        if( bytes < 1024*1024*1024*1024*1024):
            return  f"{bytes/1024/1024/1024/1024:4.0f}" + " TB"
        else:
            return f"{bytes:5.0f}" + "  B"