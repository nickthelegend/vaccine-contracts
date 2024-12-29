from beaker import client, sandbox
from vaccine import app, get_app_state_val, set_app_state_val, set_admin, get_admin, get_total_stores, set_total_stores, set_total_global_vaccine, get_total_global_vaccine, get_local_role, set_local_role, set_vaccine_quantity,readItem
from beaker.consts import algo
from algokit_utils.logic_error import LogicError

app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)


print(f"The Admin is {sender.address}")
app_id, addr, txid = app_client.create()
app_client.fund(10 * algo)

print("App ID: ", app_id)

try:
    app_client.call(set_app_state_val, v=1)
except:
    print("Failed as expected since this state is static")


try:
    app_client.call(set_admin, new_admin=sender.address)
except:
    print("Failed While setting the new_admin address")


result = app_client.call(get_app_state_val)
print("App State: ", result.return_value)


result = app_client.call(get_admin)
print("App State: ", result.return_value)



try: 
    app_client.call(set_total_stores, v=20)

except:
    print("Failed to set the total number of stores")



result = app_client.call(get_total_stores)
print(f"Total Number of stores are : {result.return_value}")

try: 
    app_client.call(set_total_global_vaccine, v=20)

except:
    print("Failed to set the total number of stores")



result = app_client.call(get_total_global_vaccine)
print(f"Total Number of global available vaccine are : {result.return_value}")







# we have to opt in for setting the local state values


app_client.opt_in()

try: 
    app_client.call(set_local_role, v="Admin")

except:
    print("Failed to set the Role")



result = app_client.call(get_local_role)
print(f"The Role of this account is : {result.return_value}")











# app_client.call(set_vaccine_quantity, store_id="sad",vaccine_name="Covaccine",vaccineManufacturer="sad",desc="sad",vaccine_id=123,quantity=120, boxes=[(app_client.app_id, "sad")])   

# try:
#     value = app_client.call(
#         readItem, store_id="sad", boxes=[(app_client.app_id, "sad")]
#     )
#     print(value.return_value)
# except LogicError as e:
#     print("Apple box no longer exists")

import json

# Define the Python object properly
py_object = {
    "store": [
        {"name": "sad", "desc": "sad", "quantity": 23},
        {"name": "asd", "desc": "asd", "quantity": "23"}
    ]
}

# Encoding to JSON
json_string = json.dumps(py_object)

# Output the JSON string and its type
print(json_string)
print(type(json_string))


app_client.call(set_vaccine_quantity, store_id="sad",vaccine_data=json_string,quantity=120, boxes=[(app_client.app_id, "sad")])   






import time
time.sleep(30)


try:
    value = app_client.call(
        readItem, store_id="sad", boxes=[(app_client.app_id, "sad")]
    )
    print(value.return_value)
except LogicError as e:
    print("Apple box no longer exists")

