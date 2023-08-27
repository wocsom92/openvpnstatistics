import asyncio
from openVpnParser import OpenVpnParser
from connections_db import ConnectionDB
from user import User
from config import Config
from web_generator import WebGenerator

async def ip_retriever():
    while True:
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_ip_table()
        connectionDb.update_missing_connections()
        await asyncio.sleep(Config.ip_update_interval)

async def db_clean():
    while True:
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.remove_old_connections()
        connectionDb.remove_unused_ips_connections()
        connectionDb.vacuum()
        await asyncio.sleep(Config.db_clean_interval)

async def output_web_file_generator():
    while True:
        webGenerator = WebGenerator( Config.web_file_path )
        webGenerator.generate()
        await asyncio.sleep(Config.output_file_write_interval)

async def file_parse():
    while True:
        parser = OpenVpnParser()
        data = parser.parseOpenVpnStatus(Config.input_file_name)    
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_connection_table()
        for connection in data:
            existing = connectionDb.select_connection(connection.common_name, connection.connected_since)
            if existing: 
                connectionDb.update_connection(connection)
            else:
                connectionDb.insert_connection(connection)
        await asyncio.sleep(Config.input_file_parse_interval)

async def main():
    Config.production()
    tasks = [
        asyncio.create_task(file_parse()),
        asyncio.create_task(db_clean()),
        asyncio.create_task(ip_retriever()),
        asyncio.create_task(output_web_file_generator())
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())