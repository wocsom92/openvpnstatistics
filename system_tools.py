import psutil
from config import Config

class SystemTools:
    def get_ram_percentage(self):
        virtual_memory = psutil.virtual_memory()
        return virtual_memory.percent
    
    def get_disk_usage_percentage(self):
        try:
            partition_usage = psutil.disk_usage(Config.disk_to_monitor)
            usage_percentage = partition_usage.percent
            return usage_percentage
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_load_average(self):
        try:
            with open('/proc/loadavg', 'r') as loadavg_file:
                loadavg_data = loadavg_file.read().strip().split()
                loadavg_1min, loadavg_5min, loadavg_15min = map(float, loadavg_data[:3])
                return loadavg_1min, loadavg_5min, loadavg_15min
        except FileNotFoundError:
            return None
        
    def get_number_of_processes(self):
        return len(psutil.pids())