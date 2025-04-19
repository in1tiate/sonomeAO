import asyncio
import websockets
import sys
import os

class Player:
    def __init__(self, id):
        self.id = id
        self.ooc_name = "NO DATA"
        self.character = "NO DATA"
        self.showname = "NO DATA"
        self.area_id = -1

if len(sys.argv) < 3:
    print("Not enough args, provide server ip and port")
    exit

server_ip = sys.argv[1]
server_port = sys.argv[2]
server_software = ""

playerlist = {}
arealist = {}

CONNECTS = set()

async def handshake():
    async with websockets.connect(f"ws://{server_ip}:{server_port}") as websocket:
        CONNECTS.add(websocket)
        await broadcast("HI#SONOME#%")
        await broadcast("CT#Whose eyes are those eyes?##%")
        while True:
            try:
                message = await websocket.recv()
                await process(message)
                await display()
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

async def broadcast(message):
    for connect in CONNECTS:
        await connect.send(message)
                
async def process(message):
    message_contents = message.split("#")
    if message_contents[0] == "ID":
        server_software = message_contents[2]
        print(server_software)
        await broadcast("ID#SONOME#2.11.0#%")
        await broadcast("askchaa#%")
    elif message_contents[0] == "SI":
        await broadcast("RC#%")
    elif message_contents[0] == "SC":
        await broadcast("RM#%")
    elif message_contents[0] == "SM":
        await broadcast("DONE#%")
        await populate_arealist(message_contents)
    elif message_contents[0] == "PR":
        id = int(message_contents[1])
        if message_contents[2] == "0": # Add player
            new_player = Player(id)
            playerlist[id] = new_player
        elif message_contents[2] == "1": # Remove player
            del playerlist[id]
    elif message_contents[0] == "PU":
        id = int(message_contents[1])
        if message_contents[2] == "0": # ooc name
            playerlist[id].ooc_name = message_contents[3]
        elif message_contents[2] == "1": # character
            playerlist[id].character = message_contents[3]
        elif message_contents[2] == "2": # showname
            playerlist[id].showname = message_contents[3]
        elif message_contents[2] == "3": # area id
            playerlist[id].area_id = int(message_contents[3])

async def display():
    os.system('cls' if os.name == 'nt' else 'clear')

    ds = "\rその目、だれの目？\n"
    ds += f"Current server: {server_ip}:{server_port}\n"
    for area_id, area_name in arealist.items():
        ds += f"[{area_id}] {area_name}" + "\n"
        for player in playerlist.values():
            if player.area_id == area_id:
                if player.ooc_name == "Whose eyes are those eyes?":
                    continue
                ds += f"\t[{player.id}] {player.showname} ({player.character}) [{player.ooc_name}]" + "\n"
    print(ds, end='\r')

async def populate_arealist(message_contents):
    area_idx = 0
    for element in message_contents:
        if element == "SM" or element == "%":
            continue
        # is it music? if it is, ignore it
        if element.startswith("==") or element.endswith(".wav") or element.endswith(".mp3") or element.endswith(".mp4") or element.endswith(".ogg") or element.endswith(".opus"):
            continue
        arealist[area_idx] = element
        area_idx = area_idx + 1

if __name__ == "__main__":
    asyncio.run(handshake())