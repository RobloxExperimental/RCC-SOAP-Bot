import os, sys, subprocess, json, datetime, requests, discord

from xml.etree import ElementTree

from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("TOKEN")

with open('./config.json', 'r') as config:
    get = json.load(config)

prefix = get['prefix']
ip = get['ip']
port = get['port']
channel = get['channel']
admin = get['admin']

def isRunning(query):
    platform = sys.platform
    cmd = ''
    if platform == 'win32':
        cmd = 'tasklist'
    elif platform == 'darwin':
        cmd = f'ps -ax | grep {query}'
    elif platform == 'linux':
        cmd = 'ps -A'
    s = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8').lower()
    if query.lower() in s:
        return True
    return False

def screenshot(msg):
    if not os.path.exists("./screenshot.png"):
        msg.reply("An Unknown Error has occurred, Is RCC Running?")
    
    msg.channel.send(file=discord.File("./screenshot.png"))
    os.remove("./screenshot.png")

def contentVarible(content2):
    return f'''<?xml version="1.0" encoding="UTF - 8"?>
		<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns2="http://roblox.com/RCCServiceSoap" xmlns:ns1="http://roblox.com/" xmlns:ns3="http://roblox.com/RCCServiceSoap12"><SOAP-ENV:Body>
		{content2}
		</SOAP-ENV:Body></SOAP-ENV:Envelope>'''

options = {
    "hostname": ip,
    "port": port,
    "path": '',
    "headers": {
        'Accept': 'text/xml',
		'Cache-Control': 'no-cache',
		'Pragma': 'no-cache',
		'SOAPAction': 'Execute'
    }
}

def viewgame(msg):
    try:
        r = requests.post(f'{options["hostname"]}:{options["port"]}', headers=options["headers"])
        body = ElementTree.fromstring(r.text)
        image = body["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ns1:ExecuteResponse"]["ns1:ExecuteResult"][0]["ns1:value"]
        with open("./out.png", "w") as file:
            file.write(image)
        msg.channel.send(file=discord.File("./out.png"))
        content2 = """<ns1:Execute>
		<ns1:jobID>Test</ns1:jobID>
		<ns1:script>
			<ns1:name>SOAP</ns1:name>
			<ns1:script>
			return game:GetService("ThumbnailGenerator"):Click("PNG", 4000, 2000, true)</ns1:script>
			<ns1:arguments>
			</ns1:arguments>
		</ns1:script>
		</ns1:Execute>"""
        r2 = requests.post(f'{options["hostname"]}:{options["port"]}', headers=options["headers"], body=contentVarible(content2))
    except:
        msg.reply("An Unknown Error has occurred, Is RCC Running?")

async def execute(message, msg):
    if "HttpGet" in message or "HttpPost" in message or "fenv" in message or "while true do" in message or "SetUploadUrl" in message or "crash__" in message or "ModuleScript" in message or "\\77" in message or "\\11" in message or "do print(\"" in message or "do print()" in message or "math.huge do" in message or ":ExecuteScript" in message:
        msg.reply("** CENSORED CODE DETECTED! **")
    if message.startswith("`") and message.endswith("`"):
        if message.startswith("```") and message.endswith("```"):
            isLua = message.startswith("```lua")
            if isLua:
                message = message[6:]
            else:
                message = message[3:]
    else:
        message = message[1:]
    # TODO

intents = discord.Intents.all()
Client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents, help_command=None)

@Client.event
async def on_ready():
    print(f"Logged in as {Client.user}#{Client.discriminator}")

@Client.event
async def on_message(message):
    if message.author == Client.user:
        return

    if not message.channel.id == channel:
        return
    
    msg = message.content

    if msg.startswith(f"{prefix}help"):
        e = discord.Embed(title="SOAP Commands", description=f'Here are the commands for RCC SOAP Bot:\n\n{prefix}help\n{prefix}execute (<string> script) | {prefix}x\n{prefix}viewgame | {prefix}vg\n{prefix}viewconsole | {prefix}vc\n{prefix}votereset', timestamp=datetime.datetime.utcnow(), color=0x0099ff)
        e.set_author(name="RCCService.exe", icon_url="https://i.imgur.com/9cPv812.png")
        e.set_footer('Authors: Yakov, Linus man | Ported to Python3 by crimewave(cens6r)')
        
        msg.channel.send(embed=e)
    elif msg.startswith(f"{prefix}restart"):
        if msg.author.id == admin:
            msg.reply("Restarting...")
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            msg.reply("UNAUTHORIZED!")
    elif msg.startswith(f"{prefix}srestart"):
        if msg.author.id == admin:
            msg.reply("Server Restarting...")
            os.system("taskkill /im \"RCCServiceSOAP.exe\" /t")
            os.system(f"cd C:\\RCCSoap && start RCCServiceSOAP.bat {port}")
        else:
            msg.reply("UNAUTHORIZED!")
    elif msg.startswith(f"{prefix}start"):
        if msg.author.id == admin:
            msg = msg.split()
            if not msg[1]:
                msg.reply("Missing Parameter `Port`")
            status = isRunning('RCCServiceSOAP.exe')
            if status:
                msg.reply("RCCService.exe is already open.")
            os.system(f"cd C:\\RCCSoap && start RCCServiceSOAP.bat {msg[1]}")
            msg.reply(f"Started on port {msg[1]}!")
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            msg.reply("UNAUTHORIZED!")
    elif msg.startswith(f"{prefix}stop"):
        if msg.author.id == admin:
            os.system('taskkill /im "RCCServiceSOAP.exe" /t')
            msg.reply('Server Stopped!')
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            msg.reply("UNAUTHORIZED!")
    elif msg.startswith(f"{prefix}vc"):
        os.startfile("rccscreenshot.exe")
        screenshot(message)
    elif msg.startswith(f"{prefix}viewconsole"):
        os.startfile("rccscreenshot.exe")
        screenshot(message)
    elif msg.startswith(f"{prefix}vg"):
        viewgame(message)
    elif msg.startswith(f"{prefix}viewgame"):
        viewgame(message)
    elif msg.startswith(f"{prefix}x"):
        msg = msg.split()
        if not msg[1]:
            msg.reply("Missing Parameter `Script`")
        execute(msg[1], message)
    elif msg.startswith(f"{prefix}execute"):
        msg = msg.split()
        if not msg[1]:
            msg.reply("Missing Parameter `Script`")
        execute(msg[1], message)
    # TODO


    

Client.run(token)
