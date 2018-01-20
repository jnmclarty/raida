from raiblocks import RPCClient
rpc = RPCClient('http://localhost:7076')
rpc.version()
history = rpc.account_history('xrb_17fi19wanb3diz544wsiyijeo7uq6h4yu74wbxymbhr9eto5ejzgp4c6kzui', count=100)
byte_stream = [tx['amount'] for tx in history][-2::-1]
print(bytes(byte_stream).decode())
