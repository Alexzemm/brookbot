import nextcord
from nextcord.ext import commands
import wouldyourather
import eightball
import nextwave
import spotify_playlist
import bot_message
import os

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix = "-", intents = intents)
token = os.environ.get("DISCORD_TOKEN")

@client.event
async def on_ready():
    print("ready")
    client.loop.create_task(node_connect())



@client.event
async def on_nextwave_node_ready(node: nextwave.Node):
    print(f"node{node.identifier} is ready")



@client.command(aliases=["hello", "sup", "안녕", "hey"])
async def hi(ctx):
    await ctx.send("Pantsu misete morattemo yoroshii desu ka???")



@client.command(aliases=["m"])
async def msg(ctx, *, message):
    responses = bot_message.message_bot(message)

    for chunk in responses:
        await ctx.send(chunk)




@client.command(aliases=["8ball"])
async def EightBall(ctx, *, question):

    response = eightball.eb()

    await ctx.message.add_reaction("🤓")
    await ctx.send(response)



@client.command(aliases=["wouldyourather", "wyr"])
async def WouldYouRather(ctx):
    a, b = wouldyourather.wyr()
    embed = nextcord.Embed(title = "Would you rather", description = ('{} \n\n  or  \n\n {}'.format(a, b)), color = nextcord.Colour.blue())
    await ctx.send(embed = embed)
    await ctx.message.add_reaction("1️⃣")
    await ctx.message.add_reaction("2️⃣")



async def node_connect():
    await client.wait_until_ready()
    await nextwave.NodePool.create_node(bot=client, host="139.59.109.24", port=7800, password="https://discord.gg/mjS5J2K3ep")



@client.event
async def on_nextwave_track_end(player: nextwave.Player, track: nextwave.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        return await vc.play(track)

    next_song = vc.queue.get()
    await vc.play(next_song)
    embed = nextcord.Embed(title=f"Playing {next_song}", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)



@client.command(aliases=["p"])
async def play(ctx: commands.Context, *, url : str):

    url = await nextwave.YouTubeTrack.search(url, return_first=True)
    if not ctx.voice_client:
        vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)

    else:
        vc: nextwave.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(url)
        embed = nextcord.Embed(title=f"Playing {url}", color=nextcord.Colour.blue())
        await ctx.send(embed=embed)

    else:

        await vc.queue.put_wait(url)
        embed = nextcord.Embed(title=f"Queued {url}", color=nextcord.Colour.blue())
        await ctx.send(embed=embed)

    vc.ctx = ctx
    setattr(vc, "loop", False)



@client.command(aliases=["c"])
async def connect(ctx: commands.Context):
    await ctx.author.voice.channel.connect(cls=nextwave.Player)
    embed = nextcord.Embed(title="Joined voice channel", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)



@client.command(aliases=["dc"])
async def disconnect(ctx: commands.Context):
    await ctx.guild.voice_client.disconnect()
    embed = nextcord.Embed(title="Left voice channel", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)



@client.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
    else:
        vc: nextwave.Player = ctx.voice_client

    await vc.pause()
    embed = nextcord.Embed(title="Paused song", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)



@client.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
    else:
        vc: nextwave.Player = ctx.voice_client

    await vc.resume()
    embed = nextcord.Embed(title="Resumed song", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)



@client.command(aliases=["s"])
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
    else:
        vc: nextwave.Player = ctx.voice_client

    await vc.stop()
    embed = nextcord.Embed(title="Skipped song", color=nextcord.Colour.blue())
    await ctx.send(embed=embed)
    


@client.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
    else:
        vc: nextwave.Player = ctx.voice_client

    try:
        vc.loop = True
        embed = nextcord.Embed(title="Loop enabled", color=nextcord.Colour.blue())

    except:
        setattr(vc, "loop", False)


client.run(token)

