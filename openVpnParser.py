from connection import Connection

class OpenVpnParser:
    def parseOpenVpnStatus(self, file_path):
        connections = []
        with open(file_path, "r") as file:
            lines = file.readlines()
            
            for line in lines[3:]:  # Skip the header line  
                if "ROUTING TABLE" in line :
                    break
                values = line.strip().split(",")
                common_name, real_address, bytes_received, bytes_sent, connected_since = values
                connection = Connection(
                    common_name=common_name,
                    real_address=real_address,
                    bytes_received=int(bytes_received),
                    bytes_sent=int(bytes_sent),
                    connected_since=connected_since,
                    db_updated='',
                    ip_id = 0
                )
                connections.append(connection)
        return connections