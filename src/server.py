import ws, asyncio

server = ws.ServerSocket()
passages = 0

@server.on('ready')
async def on_ready():
    print(f"Server is ready listening at ws://{server.address}:{server.port}")

@server.on('connect')
async def on_connect(client, path):
    global passages
    print(f"Client at {client.remote_address} connected.")
    for i in range(10):
       await client.send(data={'passages': passages})
       await asyncio.sleep(1)
       passages += 1
       
@server.on('message')
async def on_message(message):
    print(f"{message.data}")
    print(f"Received from: {message.author.remote_address} at {message.created_at}")

@server.on('disconnect')
async def on_disconnect(client, code, reason):
    print(f"Client at {client.remote_address} disconnected with code: ", code, "and reason: ", reason)
    print(server.disconnected_clients)

@server.on("close")
async def on_close(client, code, reason):
    print(f"Client at {client.remote_address} closed connection with code: {code} and reason: {reason}")

server.listen("localhost", 3000)
