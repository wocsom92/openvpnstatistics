import sqlite3
from datetime import datetime, date, timedelta
from connection import Connection

class ConnectionDB:
    def __init__(self, db_name ):
        self.db_name = db_name + '.db'
    def create_connection_database(self):
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
                common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated = result
                return Connection(common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated)
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
                common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated = result
                connection = Connection(common_name, real_address, bytes_received, bytes_sent, connected_since, db_updated)
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

