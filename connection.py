class Connection:
    def __init__(self, common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated, ip_id):
        self.common_name = common_name
        self.real_address = real_address
        self.bytes_received = bytes_received
        self.bytes_sent = bytes_sent
        self.connected_since = connected_since
        self.db_updated = db_updated
        self.ip_id = ip_id

    def print(self):
        print("Common Name:", self.common_name)
        print("Real Address:", self.real_address)
        print("Bytes Received:", self.bytes_received)
        print("Bytes Sent:", self.bytes_sent)
        print("Connected Since:", self.connected_since)
        print("Db Updated:", self.db_updated)
        print()