import sqlite3
import os
from datetime import datetime, date, timedelta
from connection import Connection
from config import Config
from ip_info import IpInfo

class ConnectionDB:
    def __init__(self, db_name ):
        folder_name = "data"
        file_name = db_name + '.db'
        self.db_name = os.path.join(folder_name, file_name)
    def create_connection_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS connections (
                    common_name TEXT,
                    real_address TEXT,
                    bytes_received INTEGER,
                    bytes_sent INTEGER,
                    connected_since DATETIME,
                    db_updated DATETIME,
                    ip_id INTEGER,
                    PRIMARY KEY (common_name, connected_since)
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()
    
    def create_ip_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS ips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT,
                    city TEXT,
                    region TEXT,
                    country TEXT,
                    table_updated DATETIME,
                    provider TEXT
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def insert_connection(self, connection):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO connections (common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (connection.common_name, connection.real_address, connection.bytes_received, connection.bytes_sent, connection.connected_since, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def update_connection(self, data):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                UPDATE connections
                SET bytes_received = ?, bytes_sent = ?, db_updated = ?
                WHERE common_name = ? AND connected_since = ?
            ''', (data.bytes_received, data.bytes_sent, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.common_name, data.connected_since))

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def delete_connection(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                DELETE FROM connections
                WHERE common_name = ?
            ''', (common_name,))

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def select_connection(self, common_name, connected_since):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT * FROM connections
                WHERE common_name = ? AND connected_since = ?
            ''', (common_name, connected_since))

            result = c.fetchone()

            if result:
                common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated, ip_id = result
                return Connection(common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated, ip_id)
            else:
                return None
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None
        finally:
            conn.close()

    def select_all_connections(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT * FROM connections
            ''')

            results = c.fetchall()

            connections = []
            for result in results:
                common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated, ip_id = result
                connection = Connection(common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated, ip_id)
                connections.append(connection)

            return connections
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return []
        except Exception as e:
            print("An unexpected error occurred:", e)
            return []
        finally:
            conn.close()

    def select_distinct_common_names(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT DISTINCT common_name FROM connections
            ''')

            results = c.fetchall()

            conn.close()

            common_names = [result[0] for result in results]
            return common_names
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return []
        except Exception as e:
            print("An unexpected error occurred:", e)
            return []

    def select_sum_bytes_for_common_name(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT SUM(bytes_sent), SUM(bytes_received)
                FROM connections
                WHERE common_name = ?
            ''', (common_name,))

            result = c.fetchone()

            conn.close()

            sum_bytes_sent, sum_bytes_received = result
            return sum_bytes_sent, sum_bytes_received
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None, None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None, None
    
    def select_last_seen(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT MAX(db_updated)
                FROM connections
                WHERE common_name = ?
            ''', (common_name,))

            result = c.fetchone()

            conn.close()

            if result and result[0]:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None

    def select_sum_bytes_for_current_day(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Get the current date
            current_date = datetime.now().strftime('%Y-%m-%d')

            c.execute('''
                SELECT SUM(bytes_sent), SUM(bytes_received)
                FROM connections
                WHERE DATE(db_updated) = ? AND common_name = ? -- Convert datetime to date for comparison
            ''', (current_date,common_name))

            result = c.fetchone()
            conn.close()

            sum_bytes_sent, sum_bytes_received = result
            if sum_bytes_sent == None:
                sum_bytes_sent = 0
            if sum_bytes_received == None:
                sum_bytes_received = 0
            return sum_bytes_sent, sum_bytes_received
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None, None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None, None
        
    def select_sum_bytes_for_last_week(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Calculate the date one week ago from today
            one_week_ago = datetime.now() - timedelta(weeks=1)

            c.execute('''
                SELECT SUM(bytes_sent), SUM(bytes_received)
                FROM connections
                WHERE db_updated >= ? AND common_name = ? -- Filter by date from one week ago
            ''', (one_week_ago, common_name))

            result = c.fetchone()

            conn.close()

            sum_bytes_sent, sum_bytes_received = result
            if sum_bytes_sent == None:
                sum_bytes_sent = 0
            if sum_bytes_received == None:
                sum_bytes_received = 0
            return sum_bytes_sent, sum_bytes_received
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None, None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None, None

    def select_sum_bytes_for_last_month(self, common_name):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Calculate the date one month ago from today
            one_month_ago = datetime.now() - timedelta(days=30)

            c.execute('''
                SELECT SUM(bytes_sent), SUM(bytes_received)
                FROM connections
                WHERE db_updated >= ?  AND common_name = ?-- Filter by date from one month ago
            ''', (one_month_ago, common_name))

            result = c.fetchone()

            conn.close()

            sum_bytes_sent, sum_bytes_received = result
            if sum_bytes_sent == None:
                sum_bytes_sent = 0
            if sum_bytes_received == None:
                sum_bytes_received = 0
            return sum_bytes_sent, sum_bytes_received
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None, None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None, None

    def remove_old_connections(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            delta = datetime.now() - timedelta(days=Config.db_clean_how_many_days_keep_data)
            threshold_date = delta.strftime("%Y-%m-%d %H:%M:%S")

            c.execute('''
                DELETE FROM connections WHERE db_updated < ?
            ''', (threshold_date,))

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()
    
    def remove_unused_ips_connections(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            delta = datetime.now() - timedelta(days=Config.db_clean_how_many_days_keep_data)
            threshold_date = delta.strftime("%Y-%m-%d %H:%M:%S")

            c.execute('''
                delete from ips where id in(select id from ips where id not in( select distinct ip_id from connections))
            ''')

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()
    
    def vacuum(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                VACUUM;
            ''')

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def get_list_of_unassigned_ips_from_connections(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT distinct SUBSTR(real_address, 1, INSTR(real_address, ':') - 1) AS result FROM connections WHERE ip_id is NULL;
            ''')

            result = c.fetchall()

            conn.close()

            return result

        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None
    
    def insert_ip_location(self, ip, country, region, city, provider):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO ips (ip, country, region, city, table_updated, provider)
                VALUES (?, ?, ?, ?, ? , ?)
            ''', (ip, country, region, city, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), provider))
            
            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()

    def select_ip_id(self, ip):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT id
                FROM ips
                WHERE ip LIKE ?
            ''', (ip, ))

            result = c.fetchone()

            conn.close()

            if result and result[0]:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None
        
    def update_ip_ids(self, ip, id):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                UPDATE connections
                SET ip_id = ?
                WHERE SUBSTR(real_address, 1, INSTR(real_address, ':') - 1) LIKE ?
            ''', (id, ip))

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            conn.close()
        
    def match_ips_with_location(self, ips):
        for ip in ips:
            ip = ip[0]
            location_data = IpInfo.get_ip_location(ip)
            if(location_data):
                if(self.select_ip_id(ip) == None):
                    self.insert_ip_location(ip, location_data.get("country", "Unknown Country"), 
                                            location_data.get("region", "Unknown Region"), 
                                            location_data.get("city", "Unknown City"), 
                                            location_data.get("org", "Unknown Provider"),
                                            )
                self.update_ip_ids(ip, self.select_ip_id(ip))
    def update_missing_connections(self):
        ips = self.get_list_of_unassigned_ips_from_connections()
        self.match_ips_with_location(ips)

    def selectLocations(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                select distinct  country, region, city, provider from ips join connections 
on connections.ip_id = ips.id
where  DATE(db_updated) >= DATE('now', '-7 days');
            ''' )

            result = c.fetchall()

            conn.close()

            if result:
                return result
            else:
                return None
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None
        
    def ipCount(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute('''
                SELECT SUM(group_count) AS total_distinct_ips
FROM (
    SELECT COUNT(DISTINCT ips.id) AS group_count
    FROM ips
    JOIN connections ON connections.ip_id = ips.id
    WHERE DATE(connections.db_updated) >= DATE('now', '-7 days')
    GROUP BY ips.country, ips.region, ips.city
) AS grouped_counts;

            ''' )

            result = c.fetchone()

            conn.close()

            if result:
                return result
            else:
                return None
        except sqlite3.Error as e:
            print("SQLite error occurred:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None