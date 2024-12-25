from beaker import client, sandbox
from vaccine import app, get_app_state_val, set_app_state_val, set_admin

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

print("App ID: ", app_id)

try:
    app_client.call(set_app_state_val, v=1)
except:
    print("Failed as expected since this state is static")


# try:
app_client.call(set_admin, new_admin=sender.address)
# except:
print("Failed as expected since this state is static")


result = app_client.call(get_app_state_val)
print("App State: ", result.return_value)
