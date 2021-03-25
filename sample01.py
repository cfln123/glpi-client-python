from glpi_client import GLPIClient
from os import environ
from json import dumps

glpi_client = GLPIClient(environ['URL'], environ['APP_TOKEN'], environ['USER_TOKEN'], verify=False)

glpi_client.init_session()

result0 = glpi_client.get_asset('Computer', 4753, { 'with_devices': '' })
print(result0)

result1 = glpi_client.get_assets('Computer', { 'id': 4754 }, { 'with_devices': '' })
print(result1)

result2 = glpi_client.add_assets('Ticket', [
  { 'name': 'Sample 01', 'content': 'Testing' },
  { 'name': 'Sample 01', 'content': 'Testing 2' }
])
print(result2)

result3 = glpi_client.add_assets('Ticket', { 'name': 'Sample 01', 'content': 'Testing 3' })
print(result3)

result4 = glpi_client.update_assets('Ticket', [
  { 'id': result2[0]['id'], 'content': 'Testing 1 - modified' },
  { 'id': result2[1]['id'], 'content': 'Testing 2 - modified' }
])
print(result4)

result5 = glpi_client.update_assets('Ticket', { 'id': result3[0]['id'], 'content': 'Testing 3 - modified' })
print(result5)

result6 = glpi_client.add_assets('Item_Ticket', { 'itemtype': 'Computer', 'items_id': result0['id'], 'tickets_id': result2[0]['id'] })
print(result6)

result7 = glpi_client.add_assets('Item_Ticket', { 'itemtype': 'Computer', 'items_id': result1[0]['id'], 'tickets_id': result2[1]['id'] })
print(result7)

glpi_client.kill_session()