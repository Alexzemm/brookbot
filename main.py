import discord
from discord.ext import commands
import wouldyourather
import eightball
import bot_message
import yt_dlp as ydl
import urllib.parse
import asyncio
from collections import deque

intents = discord.Intents.all()
client = commands.Bot(command_prefix="-", intents=intents)

server_queues = {}


def get_stream_url(query):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'no_warnings': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        try:
            result = ydl_instance.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                entry = result['entries'][0]
                return {
                    'url': entry['url'],
                    'title': entry['title'],
                    'duration': entry.get('duration', 0)
                }
            else:
                return None
        except Exception as e:
            print(f"yt-dlp error: {e}")
            return None


def get_queue(guild_id):
    if guild_id not in server_queues:
        server_queues[guild_id] = {
            'queue': deque(),
            'current': None,
            'is_playing': False
        }
    return server_queues[guild_id]


async def play_next(voice_client, guild_id):
    queue_data = get_queue(guild_id)
    
    if queue_data['queue']:
        next_song = queue_data['queue'].popleft()
        await play_song(voice_client, next_song, guild_id)
    else:
        queue_data['current'] = None
        queue_data['is_playing'] = False


async def play_song(voice_client, song_info, guild_id):
    queue_data = get_queue(guild_id)
    queue_data['current'] = song_info
    queue_data['is_playing'] = True
    
    try:
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        audio_source = discord.FFmpegPCMAudio(song_info['url'], **FFMPEG_OPTIONS)
        
        def after_playing(error):
            if error:
                print(f'Player error: {error}')
            else:
                print(f'Finished playing: {song_info["title"]}')
            
            asyncio.run_coroutine_threadsafe(play_next(voice_client, guild_id), client.loop)
        
        voice_client.play(audio_source, after=after_playing)
        print(f"Now playing: {song_info['title']}")
        
    except Exception as e:
        print(f"Play error: {e}")
        queue_data['is_playing'] = False


@client.event
async def on_ready():
    print("Bot is ready!")


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
    embed = discord.Embed(title="Would you rather", description=('{} \n\n  or  \n\n {}'.format(a, b)), color=discord.Color.blue())
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("1️⃣")
    await ctx.message.add_reaction("2️⃣")


@client.command(aliases=["p"])
async def play(ctx: commands.Context, *, query: str):
    if not ctx.author.voice:
        embed = discord.Embed(title="You need to be in a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    voice_channel = ctx.author.voice.channel
    guild_id = ctx.guild.id
    queue_data = get_queue(guild_id)
    
    if not ctx.voice_client:
        voice_client = await voice_channel.connect()
    else:
        voice_client = ctx.voice_client

    print(f"Searching for: {query}")
    
    searching_embed = discord.Embed(title=f"🔍 Searching for: {query}", color=discord.Color.yellow())
    search_msg = await ctx.send(embed=searching_embed)
    
    try:
        stream_info = get_stream_url(query)
        if not stream_info:
            embed = discord.Embed(title="No results found!", color=discord.Color.red())
            await search_msg.edit(embed=embed)
            return
            
        print(f"Found: {stream_info['title']}")
        
    except Exception as e:
        print(f"Search error: {e}")
        embed = discord.Embed(title=f"Search failed: {e}", color=discord.Color.red())
        await search_msg.edit(embed=embed)
        return

    if queue_data['is_playing'] and voice_client.is_playing():
        queue_data['queue'].append(stream_info)
        embed = discord.Embed(
            title=f"📝 Queued: {stream_info['title']}", 
            description=f"Position in queue: {len(queue_data['queue'])}", 
            color=discord.Color.blue()
        )
        await search_msg.edit(embed=embed)
        print(f"Queued: {stream_info['title']} (Position: {len(queue_data['queue'])})")
    else:
        # Play immediately
        await play_song(voice_client, stream_info, guild_id)
        embed = discord.Embed(title=f"▶️ Playing: {stream_info['title']}", color=discord.Color.green())
        await search_msg.edit(embed=embed)


@client.command(aliases=["c"])
async def connect(ctx: commands.Context):
    if not ctx.author.voice:
        embed = discord.Embed(title="You need to be in a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
        

    await ctx.author.voice.channel.connect()
    embed = discord.Embed(title="Joined voice channel", color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command(aliases=["dc"])
async def disconnect(ctx: commands.Context):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title="Left voice channel", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Not connected to a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        embed = discord.Embed(title="Not connected to a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        embed = discord.Embed(title="Paused song", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Nothing is playing!", color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        embed = discord.Embed(title="Not connected to a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        embed = discord.Embed(title="Resumed song", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Nothing is paused!", color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command(aliases=["s"])
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        embed = discord.Embed(title="Not connected to a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    guild_id = ctx.guild.id
    queue_data = get_queue(guild_id)
    
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        embed = discord.Embed(title="⏭️ Skipped song", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Nothing is playing!", color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
async def status(ctx: commands.Context):
    if not ctx.voice_client:
        embed = discord.Embed(title="Not connected to a voice channel!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    guild_id = ctx.guild.id
    queue_data = get_queue(guild_id)
    voice_client = ctx.voice_client
    
    current_song = queue_data['current']['title'] if queue_data['current'] else "None"
    queue_length = len(queue_data['queue'])
    
    status_info = f"""
    **Connected:** {voice_client.is_connected()}
    **Playing:** {voice_client.is_playing()}
    **Paused:** {voice_client.is_paused()}
    **Current Song:** {current_song}
    **Queue Length:** {queue_length}
    """
    
    embed = discord.Embed(title="Player Status", description=status_info, color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command(aliases=["q", "queue"])
async def show_queue(ctx: commands.Context):
    guild_id = ctx.guild.id
    queue_data = get_queue(guild_id)
    
    if not queue_data['queue']:
        embed = discord.Embed(title="Queue is empty!", color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    
    queue_list = []
    for i, song in enumerate(queue_data['queue'], 1):
        queue_list.append(f"{i}. {song['title']}")
    
    if len(queue_list) > 10:
        queue_list = queue_list[:10]
        queue_list.append(f"...and {len(queue_data['queue']) - 10} more")
    
    embed = discord.Embed(
        title=f"🎵 Queue ({len(queue_data['queue'])} songs)",
        description="\n".join(queue_list),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@client.command()
async def clear(ctx: commands.Context):
    guild_id = ctx.guild.id
    queue_data = get_queue(guild_id)
    
    queue_data['queue'].clear()
    embed = discord.Embed(title="🗑️ Queue cleared!", color=discord.Color.green())
    await ctx.send(embed=embed)


client.run("MTEyMDc0ODc3NjI4MjQxMTEzOA.GGkDD-.bUE1DHCEJDJb77nQo9nc2MSZt3CtQhVKVXaCBY")
