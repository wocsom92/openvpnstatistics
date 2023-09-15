import asyncio
from openVpnParser import OpenVpnParser
from connections_db import ConnectionDB
from config import Config
from web_generator import WebGenerator

async def ip_retriever():
    while True:
        await asyncio.sleep(Config.ip_update_interval)
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_ip_table()
        connectionDb.update_missing_connections()  

async def sys_resource_monitor():
    while True:
        await asyncio.sleep(Config.sys_update_interval)
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.create_system_table()
        connectionDb.update_system_resources()
        
async def db_clean():
    while True:
        await asyncio.sleep(Config.db_clean_interval)
        connectionDb = ConnectionDB(Config.db_file_mame)
        connectionDb.clean_connection_table()
        connectionDb.clean_ips_table()
        connectionDb.clean_system_resources_table()
        connectionDb.vacuum()     

async def output_web_file_generator():
    while True:
        await asyncio.sleep(Config.output_file_write_interval)
        webGenerator = WebGenerator( Config.web_file_path )
        webGenerator.generate()
        

async def file_parse():
    while True:
        await asyncio.sleep(Config.input_file_parse_interval)
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

async def main():
    #Config.production()
    Config.test()
    tasks = []
    tasks.append(asyncio.create_task(file_parse()))
    tasks.append(asyncio.create_task(db_clean()))
    tasks.append(asyncio.create_task(output_web_file_generator()))
    if(Config.location_info):
        tasks.append(asyncio.create_task(ip_retriever()))
    tasks.append(asyncio.create_task(sys_resource_monitor()))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())