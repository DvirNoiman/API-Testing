import requests
import json
import pytest

url = 'http://localhost:8000'
data = {"username": "test", "password": "1234"}
ids = []  # for collecting the object ids for future uses if needed

# login (getting access token)
# ----------------------------
print('Login')
res = requests.post(url=url + '/api/auth', json=data)

print('Requesting Token:', end="")
token = json.loads(res.text)['access_token']
print(f'(recieved){token}')

# setting header
# --------------
header = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}


# receiving a list of poly data
# -----------------------------
polyDataList = json.loads(requests.get(url=url+'/api/poly', headers=header).text)
print(f'There are {len(polyDataList)} existing objects')

for l in polyDataList:
    # parsing data from each of the already existing objects
    body = {'data': l['data']}
    objectId = l['object_id']
    ids.append(objectId)

# creating a new object
obj = requests.post(url=url + '/api/poly', json=body, headers=header)
text_dict = json.loads(obj.text)
objectId = text_dict['id']

# checks if created object exists
obj = requests.get(url=url + f'/api/poly/{objectId}', headers=header)
print(f'Object ID: {objectId}  created ', end='')
if obj.status_code == 200:
    print('Successfully')
else:
    print("unsuccessfully !")


# deleting an object
obj = requests.delete(url=url + f'/api/poly/{objectId}', headers=header)
if obj.reason == 'OK' and obj.text == '""\n':
    # Trying to retrieve the deleted poly data
    # ----------------------------------------
    obj = requests.get(url=url + f'/api/poly/{objectId}', headers=header)
    print(f'Object ID: {objectId} deleted ', end='')
    if 'Not Found' in json.loads(obj.text)['error']:
        print('Successfully')
    else:
        print("unsuccessfully !")

