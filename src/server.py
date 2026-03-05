import json
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription

from app import App, Listen
from mouse import Coords, devices

app = App()

async def index(request):
    with open("assets/html/index.html") as f:
        return web.Response(text=f.read(), content_type="text/html")

async def listen(request):
    params = await request.json()
    d = next((d for d in devices() if d.path == params["path"]), None)

    if d is None:
        return web.Response(
            content_type="application/json",
            text=json.dumps({
                "message": 'Device not found',
            }),
            status=500
        )

    def callback(listen: Listen, coords: Coords):
        listen.channel.send(json.dumps({
            'name': 'new-coords',
            'data': coords
        }))

    try:
        #app.observer_mouse(d, callback)
        return web.Response()
    except Exception as e:
        print(e)
        return web.Response(
            content_type="application/json",
            text=json.dumps({
                "message": 'Server can not connect to device',
            }),
            status=500
        )



async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()

    await app.add_peer(pc)

    #@pc.on("datachannel")
    #def on_datachannel(channel):
    #    print("Data Channel opened", channel.label)
    #    #app.add_listener(pc, channel)
    #    #try:
    #    #    d = devices_to_dict(devices())
    #    #    channel.send(json.dumps({
    #    #        'name': 'list-devices',
    #    #        'data': d
    #    #    }))
    #    #except Exception as e:
    #    #    print(e)

    #    @channel.on("message")
    #    def on_message(message):
    #        event = json.loads(message)
    #        if event['name'] == 'move-mouse':
    #            move_mouse(event['data']['x'], event['data']['y'])
    #        #print("Mensaje recibido:", message)
    #        #channel.send("Echo: " + message)

    #    for c in controllers:
    #        con = c(channel)
    #        con.register()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
    )

async def on_shutdown(_):
    await app.destroy()

async def on_startup(_):
    await app.start()

server = web.Application()
server.router.add_post("/offer", offer)
server.router.add_post("/listen", listen)
server.router.add_get("/", index)
server.on_startup.append(on_startup)
server.on_shutdown.append(on_shutdown)

web.run_app(server, port=3030)
