import ws, asyncio
from gpiozero import Button

server = ws.ServerSocket()
passages = 0
button = Button(10)


@server.on('connect')
async def on_connect(client, path):
    global passages
    print(f"Client at {client.remote_address} connected.")
    while True:
       await client.send(data={'passages': passages})
       button.wait_for_press()
       await asyncio.sleep(1)    # Antibouncing
       passages += 1

server.listen("0.0.0.0", 3000)
