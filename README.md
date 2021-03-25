# glpi-python-client

GLPI API's client written in Python.

The requests are made the directly and has support to pagination.
This client is an alternative if you do not want use the GLPI API's search engine, otherwise check the [glpi-sdk-python](https://github.com/truly-systems/glpi-sdk-python).

# Installation

## PyPi

Work in progress.

## Shell

```shell
git clone https://github.com/cfln123/glpi-client-python.git
cd glpi-client-python
pip install -r requirements.txt
cp glpi_client.py /project_folder
```

# Usage

First step is you create an instance and init a session using the url, app token and the user token.

```python
from glpi_client import GLPIClient
from os import environ

glpi_client = GLPIClient(url=environ['URL'], app_token=environ['APP_TOKEN'], user_token=environ['USER_TOKEN'])
glpi_client.init_session()
```

## Verify the SSL Certificate 
The verification is enabled by default, you can either disable by its to "False" or using a custom certificate by specifying the path.

```python
glpi_client = GLPIClient(..., verify=True) # default
glpi_client = GLPIClient(..., verify=False) # disabled
glpi_client = GLPIClient(..., verify="/path-to-certificate") # custom
```

Once the session is initiated you'll be to the following requests

## Get an single item by id

### Parameters:

- name: Type of the item (required)
- id: ID of the item (required)
- params: API parameters, [see](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md#get-an-item).

```python
computer = glpi_client.get_asset('Computer', 4753, { 'with_devices': '' })
```

## Search items by field's value

### Parameters:

- name: Type of the item (required)
- text_params: searched fields
- params: API parameters, [see](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md#get-an-item).
- max_range: Number of items retrieved in each request (default: 100).

```python
computers = glpi_client.get_assets('Computer', { 'id': 4754 }, { 'with_devices': '' }, 10)
```

## Add new items (one or more)

### Parameters:

- name: Type of the item (required)
- assets: items (required), [see](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md#add-items).

```python
ticket  = glpi_client.add_assets('Ticket', { 'name': 'Sample 01', 'content': 'Testing' })
tickets = glpi_client.add_assets('Ticket', [
  { 'name': 'Sample 02', 'content': 'Testing' },
  { 'name': 'Sample 03', 'content': 'Testing' }
])
```

## Update items (one or more)

### Parameters:

- name: Type of the item (required)
- assets: items, [see](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md#update-items).

```python
glpi_client.update_assets('Ticket', [{ 'id': result3[0]['id'], 'content': 'Testing 3 - modified' }])
```

## Delete items

Work in progress

## Kill session (one or more)

```python
glpi_client.kill_session()
```

# Example

```python
from glpi_client import GLPIClient
from os import environ
from json import dumps

glpi_client = GLPIClient(environ['URL'], environ['APP_TOKEN'], environ['USER_TOKEN'])
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
```