import os, urllib, discord, json, math, os.path, random, glob, colorama, requests, string
from discord.ext import tasks, commands
#A few var you can change:
prefix = "x!" #You should change the help command if you changed the prefix
#You have to put in a token in the token.txt file




client = commands.Bot(commands.when_mentioned_or(prefix))
token_file = open("./token.txt", 'r')
token = token_file.read()
client.remove_command('help')

#Current Version:
version = "1.2"

#Check update
from colorama import Fore
from colorama import Style
colorama.init()
url = 'https://raw.githubusercontent.com/Braslerl/version/main/ihs77WPZRmMclI02'
output = requests.get(url).text
output.replace("\n", " ")
if float(output) > float(version):
    print(Fore.YELLOW + "Your should upgrade your version.(https://github.com/Braslerl/Economy-Bot-Discord)" + Style.RESET_ALL)
    print(Fore.YELLOW + "Your version is "+str(version)+" but the newest version is "+output + Style.RESET_ALL)
    print(Fore.YELLOW + "In this folder is a file called update.py, you can run it to perform an autoupdate."+ Style.RESET_ALL)   
else:
    print(Fore.GREEN + "You are using the latest Version" + Style.RESET_ALL)



@client.event
async def on_ready():
    activity = discord.Game(name="Prefix: "+prefix, type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print(f'{client.user.name} has connected to Discord!')


@client.command()
async def mention_ping(self, ctx, member : discord.Member):
    await ctx.send(f"PONG {member}")






#Command.work
@client.command()
async def work(ctx):
    pfad = "./jobs/"
    cur_job = get_job(ctx.author)
    cur_job2 = get_job(ctx.author).split("-")
    cur_job_xp = get_job_xp(ctx.author)
    antwort = random.choice(open("./jobs/"+cur_job+"/answers").readlines())
    embed=discord.Embed(title=cur_job2[1], description=antwort, color=discord.Color.blue())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Check you balance")
    await ctx.send(embed=embed)
    mehr_xp = random.randrange(1, 5)
    neue_xp = int(cur_job_xp)+mehr_xp
    if int(cur_job_xp) < 100:
        cur_job_xp_erste_zahl = 0
    else:
        cur_job_xp_erste_zahl = str(cur_job_xp)[0]
    if int(neue_xp) > 600:
        await ctx.send("You're in pension")
    if neue_xp < 100:
        set_job_xp(ctx.author, str(100))
        neue_xp = 100
    else:
        set_job_xp(ctx.author, str(neue_xp))
    if neue_xp < 100:
        erste_zahl = 0
    else:
        erste_zahl = str(neue_xp)[0]
    datei_gehalt = open("./jobs/"+cur_job+"/price")
    konto_alt = get_balance(ctx.author)
    set_balance(ctx.author, str(int(konto_alt)+int(datei_gehalt.read())))
    subfolders = [f for f in os.listdir(pfad) if os.path.isdir(os.path.join(pfad, f))]
    if cur_job_xp_erste_zahl is not erste_zahl:
        job = subfolders[int(erste_zahl)].split("-")
        await ctx.send("Get the champain hans, you got a better job: **"+job[1]+"**")
        set_job(ctx.author, subfolders[int(erste_zahl)])





#Command.jobs
@client.command()
async def jobs(ctx):
    pfad = "./jobs/"
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "w")
    subfolders = [f for f in os.listdir(pfad) if os.path.isdir(os.path.join(pfad, f))]
    for datei in subfolders:
        datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "a")
        datei2 = open(pfad+datei+"/price", 'r')
        preis = datei2.read()
        datei3 = open(pfad+datei+"/emoji", 'r')
        emoji = datei3.read()
        datei4 = open(pfad+datei+"/info", 'r')
        info = datei4.read()
        datei_temp.write(emoji+"**"+(datei)+"**"+ " ~ Salary: "+preis+"\n "+info+"\n\n")
        datei2.close()
        datei3.close()
        datei_temp.close()
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "r")
    embed=discord.Embed(title="All jobs:", color=discord.Color.blue())
    embed.add_field(name="Here you are:", value=datei_temp.read(), inline=True)
    embed.set_footer(text="You can get better jobs by working harder")
    await ctx.send(embed=embed)



#Command.job
@client.command()
async def job(ctx, member: discord.User = None):
    if member is None:
        user = ctx.author
    else:
        user = member
    nummer = get_job_xp(user)
    job = get_job(user)
    job_splitted = job.split("-")
    progressbar_url = ("http://braslerl-api.herokuapp.com/progressbar?number="+str(nummer)[-2]+str(nummer)[-3]+"&back_color=2c2f33&front_color=99aab5")
    embedVar = discord.Embed(title="Job:", description="You are: "+(job_splitted)[1]+"\n **Progress until you get a better job:**", color=0x03FF0B)
    embedVar.set_image(url=progressbar_url)
    embedVar.set_author(name=user.name, icon_url=user.avatar_url)
    #embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embedVar)












#Command.calculate
@client.command()
async def calculate(ctx):
    nummer_1 = random.randrange(1, 100)
    nummer_2 = random.randrange(1, 100)
    nummer_3 = random.randrange(1, 100)
    zeichen = random.randrange(1,2)
    if zeichen is 1:
        rechenoperation = "+"
        ergebnis = (nummer_1 + nummer_2)
    else:
        rechenoperation = "-"
        ergebnis = (nummer_1 - nummer_2)
    aufgabe = ("`"+str(nummer_1 )+ rechenoperation+ str(nummer_2)+"`")
    await ctx.send("Solve this: "+ aufgabe)
    check = message_check(author=ctx.author, channel=ctx.channel,)
    msg = await client.wait_for("message", timeout=20.0, check=check)
    ist_zahl = (msg.content).isdigit()
    if ist_zahl is False:
        await ctx.send("It has to be a f*cking number dumpass")
    else:
        if int(msg.content) is int(ergebnis):
            paid = int(300*(nummer_3/100)+ergebnis)
            int(get_balance(ctx.author))
            set_balance(ctx.author, str(int(get_balance(ctx.author))+int(paid)))
            await ctx.send("You got paid `"+str(paid)+"`")
        else:
            int(get_balance(ctx.author))
            set_balance(ctx.author, str(int(get_balance(ctx.author))+40))
            await ctx.send("We are not happy with your work, we gave you only 40")


from collections.abc import Sequence

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)
def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check




#Command.help
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Commands:", color=discord.Color.blue())
    embed.add_field(name="Fun:", value="`meme` - will send a meme into this channel \n`trash` - generate an trash image \n `glitch` - generate an glitched image from you or the person you mentioned \n `gayrate` - say how much gay someone is", inline=True)
    embed.add_field(name="Money:", value="`work` - you can work and get a little salary \n `gamble` - you can win or loose \n`balance` - shows the balance from you or the person you mentioned \n `beg` - maybe you get some money \n`fishing` - you can go fishing \n `rob` - you can try to rob the person you mentioned\n `claim` - use this to claim a code (only the Owner can generate them) \n`hunting` - you go hunting", inline=False)
    embed.add_field(name="Items:", value="`shop` - shows all items \n`item` - display more item-info \n `buy` - here you can buy an item \n `sell` - here you can sell an item \n `inventar` - shows what you own", inline=False)
    embed.add_field(name="Other:", value="`ping` - shows the bot ping \n`invite` - not finished yet \n `help` - will send this", inline=False)
    embed.set_footer(text="Requested by "+ctx.author.name)
    await ctx.send(embed=embed)



#Command.gamble
@client.command()
async def gamble(ctx, *, arg= None):
    if arg is None:
        await ctx.send("How much you want to gamble? `x!gamble [amount]`")
    else:
        ist_zahl = (arg).isdigit()
        if ist_zahl is False:
            await ctx.send("Submit a f*cking number dumpass")
        else:
            konto_alt = int(get_balance(ctx.author))
            if int(arg) > konto_alt:
                await ctx.send("You don't have enough money to gamble with "+str(arg))
            else:
                nummer_1 = random.randrange(100)
                if nummer_1 > 60:
                    await ctx.send("Ahahaha you lost you money")
                    int(get_balance(ctx.author))
                    set_balance(ctx.author, str(int(get_balance(ctx.author)) - int(arg)))
                else:
                    await ctx.send("Nice, you won")
                    int(get_balance(ctx.author))
                    set_balance(ctx.author, str(int(get_balance(ctx.author)) + int(arg)))






#Command.claim
@client.command()
async def claim(ctx, arg = None):
    if arg is None:
        await ctx.send("You have to submit a code idiot")
    else:
        user = ctx.author
        msg = claim_code(user, arg)    
        await ctx.send(msg)







#Command.gayrate
@client.command()
async def gayrate(ctx, arg = None):
    if arg is None:
        await ctx.send("Who is ? You have to mention him")
    else:
        text = (arg+" is "+str(random.randrange(100))+"% gay :rainbow_flag:")
        embed = discord.Embed(title="Gayrate:", description=text, color=discord.Color.blue())
        embed.set_footer(text=ctx.author.name+" asked" )
        await ctx.send(embed=embed)





#Command.create_code
@client.command(aliases=['gen_code'])
@commands.is_owner()
async def create_code(ctx, arg):
    code = get_random_string(8)
    datei = open("./codes/"+str(code), 'w')
    datei.write(arg)
    await ctx.send("Claim the code with: `x!claim "+str(code)+"` to get "+str(arg))






from glitch_this import ImageGlitcher
glitcher = ImageGlitcher()

#Command.glitch
@client.command()
async def glitch(ctx, member: discord.User = None):
    if member is None:
        member = ctx.author
    else:
        member = member
    urllib.request.urlretrieve("http://braslerl-api.herokuapp.com/glitch?url="+str(member.avatar_url), "./temp/av.png")
    glitch_img = glitcher.glitch_image('./temp/av.png', 3, color_offset=True, gif=True)
    glitch_img[0].save('./temp/image.gif',
                     format='GIF',
                     append_images=glitch_img[1:],
                     save_all=True,
                     duration=200,
                     loop=0)
    await ctx.send(file=discord.File('./temp/image.gif'))


#Command.trash
@client.command()
async def trash(ctx, member: discord.User = None):
    if member is None:
        await ctx.send("Who is trash? You have to mention him")
    else:
        urllib.request.urlretrieve("http://braslerl-api.herokuapp.com/trash?name="+((member.name).replace(' ', '%20')), "./temp/image.jpg")
        await ctx.send(file=discord.File('./temp/image.jpg'))



#Command.sell
@client.command()
async def sell(ctx, *, arg= None):
    if arg is None:
        await ctx.send("Which item you want to sell? Use `x!sell [item name]`")
    else:
        file = ("./shop/"+arg+"/")
        if os.path.isfile(file+"/info"):
            nummer1 = get_item(ctx.author, arg)
            if int(nummer1) < 1:
                await ctx.send("You don't have enough "+arg +" to sell")
            else:
                datei = open(file+"price", 'r')
                preis2 = int(datei.read())
                preis = round(((int(preis2))-int(preis2* + 0.10)), 0)
                alter_kontostand = int(get_balance(ctx.author))
                neuer_kontostand = (alter_kontostand+preis)
                set_balance(ctx.author, str(neuer_kontostand))
                anzahl_alt = get_item(ctx.author, arg)
                anzahl_neu = (int(anzahl_alt) - 1)
                set_item(ctx.author, arg, str(anzahl_neu))
                datei4 = open(file+"/emoji", "r")
                emoji = datei4.read()
                await ctx.send("You sold "+ str(emoji)+arg + " for "+str(preis))
        else:
            await ctx.send("Sry we can't find that item, maybe you misspelled it?")




#Command.inventar
@client.command(aliases=['inv'])
async def inventar(ctx):
    pfad = "./data/"+str(ctx.author.id)+"/items/"
    if not os.path.exists(pfad):
        os.makedirs(pfad)
    result = [f for f in os.listdir(pfad) if os.path.isfile(os.path.join(pfad, f))]
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "w")
    for datei in result:
        datei2 = open(pfad+datei, 'r')
        if (datei2.read()) is not str("0"):
            datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "a")
            anzahl = get_item(ctx.author, datei)
            datei3 = open("./shop/"+datei+"/emoji", 'r')
            emoji = datei3.read()
            datei_temp.write(emoji+(datei)+ " - "+anzahl+"\n")
            datei_temp.close()
    nummer = get_balance(ctx.author)
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "a")
    datei_temp.write(":money_with_wings: Money: $"+nummer)
    datei_temp.close()
    datei3 = open("./temp/"+str(ctx.author.id)+".txt")
    content = datei3.read()
    embedVar = discord.Embed(color=discord.Color.blue())
    embedVar.add_field(name="You own this items:", value=((content)), inline=True)
    embedVar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embedVar)


#Command.buy
@client.command()
async def buy(ctx, *, arg= None):
    if arg is None:
        await ctx.send("Which item you want to buy? Use `x!buy [item name]`")
    else:
        file = ("./shop/"+arg+"/")
        if os.path.isfile(file+"/info"):
            datei = open(file+"price", 'r')
            preis= int(datei.read())
            alter_kontostand = int(get_balance(ctx.author))
            if preis > alter_kontostand:
                await ctx.send("You can't afford it, it costs "+str(preis)+" but you only have "+str(alter_kontostand))
            else:
                neuer_kontostand = (alter_kontostand-preis)
                set_balance(ctx.author, str(neuer_kontostand))
                anzahl_alt = get_item(ctx.author, arg)
                anzahl_neu = (int(anzahl_alt) + 1)
                set_item(ctx.author, arg, str(anzahl_neu))
                await ctx.send("Here you go, you now have "+str(anzahl_neu)+" "+ arg)
        else:
            await ctx.send("Sry we can't find that item, maybe you misspelled it?")




#Command.item
@client.command()
async def item(ctx, *, arg= None):
    if arg is None:
        await ctx.send("Which item details do you want to see? Use `x!item [item name]`")
    else:
        file = ("./shop/"+arg+"/")
        if os.path.isfile(file+"/info"):
            datei = open(file+"info", 'r')
            datei2 = open(file+"price", 'r')
            embed=discord.Embed(title=arg, color=discord.Color.blue())
            embed.add_field(name="Information:", value=datei.read(), inline=True)
            embed.add_field(name="Price:", value=datei2.read(), inline=True)
            embed.set_footer(text="Use `x!buy [item name]` to buy it")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sry we can't find that item, maybe you misspelled it?")



#Command.shop
@client.command()
async def shop(ctx):
    pfad = "./shop/"
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "w")
    subfolders = [f for f in os.listdir(pfad) if os.path.isdir(os.path.join(pfad, f))]
    for datei in subfolders:
        datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "a")
        datei2 = open(pfad+datei+"/price", 'r')
        preis = datei2.read()
        datei3 = open(pfad+datei+"/emoji", 'r')
        emoji = datei3.read()
        datei4 = open(pfad+datei+"/info", 'r')
        info = datei4.read()
        datei_temp.write(emoji+"**"+(datei)+"**"+ " - "+preis+"\n "+info+"\n\n")
        datei2.close()
        datei3.close()
        datei_temp.close()
    datei_temp = open("./temp/"+str(ctx.author.id)+".txt", "r")
    embed=discord.Embed(title="Shop", color=discord.Color.blue())
    embed.add_field(name="Items:", value=datei_temp.read(), inline=True)
    embed.set_footer(text="Use `x!item [item name]` to see more infos for the mentioned item")
    await ctx.send(embed=embed)





#Command.hunting
@commands.cooldown(1, 90, commands.BucketType.user)
@client.command(aliases=['hunt'])
async def hunting(ctx):
    anzahl = get_item(ctx.author, "hunting rifle")
    if int(anzahl) is 0:
        await ctx.send("Dumpass, you need a hunting rifle")
    else:
        nummer_1 = random.randrange(100)
        if nummer_1 > 60:
            await ctx.send("Nice work, you got a deer. You can sell it")
            anzahl_deer = get_item(ctx.author, "deer")
            set_item(ctx.author, "deer", str(int(anzahl_deer)+1))
        else:
            nummer_1 = random.randrange(100)
            if nummer_1 > 60 and nummer_1 > 40:
                await ctx.send("Nice work, you caught a boar which is rare. You can sell it")
                anzahl_boar = get_item(ctx.author, "boar")
                set_item(ctx.author, "boar", str(int(anzahl_boar)+1))
                nummer_2 = random.randrange(100)
            else:
                if nummer_1 < 17:
                    await ctx.send("You failed and lost your hunting rifle")
                    angeln_anzahl = get_item(ctx.author, "hunting rifle")
                    set_item(ctx.author, "hunting rifle", str(int(angeln_anzahl)-1))
                else:
                    await ctx.send("You found nothing :neutral_face: ")


@hunting.error
async def fish_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=":x: Cooldown:x:", description=('You can go hunting again in {:.0f}s'.format(error.retry_after)), color=0xFF0000)
        embedVar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #embedVar.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embedVar)





#Command.fish
@commands.cooldown(1, 90, commands.BucketType.user)
@client.command()
async def fish(ctx):
    anzahl = get_item(ctx.author, "fishing rod")
    if int(anzahl) is 0:
        await ctx.send("You don't own a fishing rod, you have to buy it first")
    else:
        nummer_1 = random.randrange(100)
        if nummer_1 > 60:
            await ctx.send("Nice work, you caught a fish. You can sell it")
            anzahl_fische = get_item(ctx.author, "fish")
            set_item(ctx.author, "fish", str(int(anzahl_fische)+1))
        else:
            nummer_1 = random.randrange(100)
            if nummer_1 > 60 and nummer_1 > 40:
                await ctx.send("Nice work, you caught a **rare** fish. You can sell it")
                anzahl_fische = get_item(ctx.author, "rare fish")
                set_item(ctx.author, "rare fish", str(int(anzahl_fische)+1))
                nummer_2 = random.randrange(100)
            else:
                if nummer_1 < 20:
                    await ctx.send("You so shit in fishing. You're fishing rod broked")
                    angeln_anzahl = get_item(ctx.author, "fishing rod")
                    set_item(ctx.author, "fishing rod", str(int(angeln_anzahl)-1))
                else:
                    await ctx.send("Maybe next time :neutral_face: ")


@fish.error
async def fish_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=":x: Cooldown:x:", description=('You can go fishing again in {:.0f}s'.format(error.retry_after)), color=0xFF0000)
        embedVar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #embedVar.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embedVar)



#Command.rob
@commands.cooldown(1, 5, commands.BucketType.user)
@client.command()
async def rob(ctx, member: discord.User = None):
    if member is None:
        await ctx.send("Please mention the person you want to rob.")
    else:
        user = ctx.author
        dieb_bal = get_balance(user)
        if int(dieb_bal) < 300:
            await ctx.send("You need at least $300 to pay the target when you get caught (You have "+dieb_bal+" atm.)")
        else:
            user = member
            opfer_bal = get_balance(user)
            if int(opfer_bal) < 300:
                await ctx.send("Your taget need at least $300 (It has "+opfer_bal+" atm.)")
            else:
                nummer_1 = random.randrange(100)
                if nummer_1 > 40:
                    await ctx.send("Nice work thief, you got 300 more in your pocket now.")
                    set_balance(ctx.author, str(int(dieb_bal)+300))
                    set_balance(member, str(int(opfer_bal)-300))
                else:
                    await ctx.send("Hahaha get f*cked, you paid 300 to "+member.name+".")
                    set_balance(ctx.author, str(int(dieb_bal)-300))
                    set_balance(member, str(int(opfer_bal)+300))

@rob.error
async def rob_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=":x: Cooldown:x:", description=('You can rob someone again in {:.0f}s'.format(error.retry_after)), color=0xFF0000)
        embedVar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #embedVar.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embedVar)




#Command.Beg
@commands.cooldown(1, 90, commands.BucketType.user)
@client.command()
async def beg(ctx):
    user = ctx.author
    guthaben = get_balance(user)
    earnings = random.randrange(101)
    await ctx.send(ctx.author.mention+" got "+str(earnings)+" by begging")
    guthaben_neu = (int(guthaben) + int(earnings))
    set_balance(user, str(guthaben_neu))

@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=":x: Cooldown:x:", description=('You can beg again in {:.0f}s'.format(error.retry_after)), color=0xFF0000)
        embedVar.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #embedVar.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embedVar)



#Command.balance
@client.command(aliases=['bal'])
async def balance(ctx, member: discord.User = None):
    if member is None:
        user = ctx.author
    else:
        user = member
    nummer = get_balance(user)
    embedVar = discord.Embed(title="Balance:", description=":money_with_wings: "+nummer, color=0x03FF0B)
    embedVar.set_author(name=user.name, icon_url=user.avatar_url)
    #embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embedVar)


@client.command(pass_context = True)
@commands.is_owner()
async def say(ctx, *args):
    await ctx.send(' '.join(args))


#Command.ping
@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency*100, 1))+" ms")





#Command.meme
@client.command()
async def meme(ctx,):
    with urllib.request.urlopen("https://meme-api.herokuapp.com/gimme") as url:
        data = json.loads(url.read().decode())
    embed=discord.Embed(color=discord.Color.blue())
    embed.set_image(url=data['url'])
    embed.set_footer(text="Requested by "+ctx.author.name)
    await ctx.send(embed=embed)
    data = None





#Funktion.get_balance
def get_balance(user):
    file = ("./data/"+str(user.id)+"/balance.txt")
    pfad = ("./data/"+str(user.id))
    if os.path.isfile(file):
            datei = open(file, 'r')
            return(datei.read())
    else:
        if not os.path.exists(pfad):
            os.makedirs(pfad)
        datei2 = open("./data/"+str(user.id)+"/name.txt", 'w')
        datei2.write(user.name)
        datei2.close()
        datei = open(file, 'w')
        datei.write("0")
        datei.close()
        datei = open(file, 'r')
        return(datei.read())




#Funtion.set_balance
def set_balance(user, balance_neu):
    file = ("./data/"+str(user.id)+"/balance.txt")
    os.remove(file)
    datei = open(file, 'w')
    datei.write(balance_neu)
    datei2 = open("./data/"+str(user.id)+"/name.txt", 'w')
    datei2.write(user.name)
    datei2.close()

#Funktion.get_item
def get_item(user, itemname):
    file = ("./data/"+str(user.id)+"/items/"+itemname)
    pfad = ("./data/"+str(user.id)+"/items/")
    if os.path.isfile(file):
            datei = open(file, 'r')
            return(datei.read())
    else:
        if not os.path.exists(pfad):
            os.makedirs(pfad)
        datei = open(file, 'w')
        datei.write("0")
        return("0")

#Funktion.set_item
def set_item(user, itemname, number):
    file = ("./data/"+str(user.id)+"/items/"+itemname)
    pfad = ("./data/"+str(user.id)+"items/")
    os.remove(file)
    datei = open(file, 'w')
    datei.write(number)



#Funktion.listToString
def listToString(s):  
    str1 = "\n"  
    return (str1.join(s)) 

#Funktion.get_random_string
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)



#Funktion.claim_code
def claim_code(user, code):
    file = ("./codes/"+code)
    if os.path.isfile(file):
        datei = open(file, 'r')
        old_balance = int(get_balance(user))
        wert = (str(datei.read()))
        new_balance = (old_balance + int(wert))
        set_balance(user, str(new_balance))
        datei.close()
        os.remove(file)
        return("You claimed a "+wert+" code")
    else:
        return("Code isn't valid")






#Funtion.set_job
def set_job(user, balance_neu):
    file = ("./data/"+str(user.id)+"/job.txt")
    os.remove(file)
    datei = open(file, 'w')
    datei.write(balance_neu)
    datei2 = open("./data/"+str(user.id)+"/job.txt", 'w')
    datei2.write(user.name)
    datei2.close()


#Funktion.get_job
def get_job(user):
    file = ("./data/"+str(user.id)+"/job.txt")
    pfad = ("./data/"+str(user.id))
    if os.path.isfile(file):
            datei = open(file, 'r')
            return(datei.read())
    else:
        if not os.path.exists(pfad):
            os.makedirs(pfad)
        datei2 = open("./data/"+str(user.id)+"/name.txt", 'w')
        datei2.write(user.name)
        datei2.close()
        datei = open(file, 'w')
        datei.write("1 - Currently unemployed")
        datei.close()
        datei = open(file, 'r')
        return(datei.read())



#Funtion.set_job_xp
def set_job_xp(user, balance_neu):
    file = ("./data/"+str(user.id)+"/job_xp.txt")
    os.remove(file)
    datei = open(file, 'w')
    datei.write(balance_neu)
    datei2 = open("./data/"+str(user.id)+"/name.txt", 'w')
    datei2.write(user.name)
    datei2.close()


#Funktion.get_job_xp
def get_job_xp(user):
    file = ("./data/"+str(user.id)+"/job_xp.txt")
    pfad = ("./data/"+str(user.id))
    if os.path.isfile(file):
            datei = open(file, 'r')
            return(datei.read())
    else:
        if not os.path.exists(pfad):
            os.makedirs(pfad)
        datei2 = open("./data/"+str(user.id)+"/name.txt", 'w')
        datei2.write(user.name)
        datei2.close()
        datei = open(file, 'w')
        datei.write("0")
        datei.close()
        datei = open(file, 'r')
        return(datei.read())




client.run(token)
