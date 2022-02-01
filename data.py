import os, datetime
from uuid import uuid4
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient

TABLES_URL = "https://tanks.table.core.windows.net"

class User:
    def __init__(self, name, x, y):
        self.uuid = str(uuid4())
        self.name = name
        self.x = x
        self.y = y
        self.score = 0
        self.resources = {}

class Resource:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

def get_last_update_db():
    try:
        STORAGE_KEY = os.getenv('STORAGE_KEY')
        credential = AzureNamedKeyCredential("tanks", STORAGE_KEY)
        service = TableServiceClient(endpoint=TABLES_URL, credential=credential)
        table_name = "updatetime"
        service.create_table_if_not_exists(table_name=table_name)
        table = service.get_table_client(table_name=table_name)
        try:
            entities = table.query_entities("PartitionKey eq 'Time'")
            current = entities.next()
        except:
            print("AAAAAA")
        if current is None:
            table.create_entity({
                u'PartitionKey': "Time",
                u'RowKey': "Time",
                u'LastUpdate': datetime.now()
            })
        else:
            table.update_entity({
                u'PartitionKey': "Time",
                u'RowKey': "Time",
                u'LastUpdate': datetime.now()
            })
        return current
    except:
        return "Cannot get last update"