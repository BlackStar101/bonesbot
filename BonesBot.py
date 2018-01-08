import discord
import discord.ext.commands
from discord.ext import commands
import asyncio
from datetime import date
import random
import math
import sys
import os
import traceback
import time

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

try:
    f = open("pass.txt","r")
except:
    print('You need the bot\'s token in a TXT file called \"pass.txt\" for this code to connect to.')
runpass = f.readlines()
runpass = str(runpass)
trtlrunpass = dict.fromkeys(map(ord, '[\']'), None)
runpass = runpass.translate(trtlrunpass)


boneshelp = '**BonesBot** version PRE-ALPHA 1 by GunnerBones \n\n**!anysizelist <list size>** Gets a player\'s score based on ANY list size\n**!yes** Does nothing.\n**!rainbowrole** Creates a role with a rainbow color! Use **!activaterb** to turn on rainbow effect everytime BonesBot restarts.'

# Global Methods

rbrl = None

def is_int(a):
    try:
        a = int(a)
    except ValueError:
        return False
    else:
        return True

def check_all_perms():
    print()
    print('All servers connected to with roles:')
    for server in client.servers:
        hrole = server.me.top_role
        print(server.name + ': ' + str(hrole))

def serverstats():
    for server in client.servers:
        try:
            servname = 'bonesbot-' + server.id + '-demonlist.txt'
            f = open(servname,'a')
            sortsn = 'serverstats/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = 'bonesbot-' + server.id + '-hasdl.txt'
            f = open(servname,'a')
            sortsn = 'serverstats/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = 'bonesbot-' + server.id + '-rb.txt'
            f = open(servname,'a')
            sortsn = 'serverstats/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)



def psc(msize,mlist):
    retval = 0.0
    for i in mlist:
        adval = msize / ((msize / 5) + ((-msize / 5) + 1) * math.exp(-0.008*float(i)))
        retval = retval + adval
    return retval

def hasadmin(message):
    foundadmin = False
    for i in message.author.roles:
        if i.permissions.administrator == True:
            foundadmin = True
            return True
    if foundadmin == False:
        return False

def rbcycle(message):
    rbfn = 'serverstats/bonesbot-' + message.server.id + '-rb.txt'
    f = open(rbfn,"r")
    if f.readlines() == "":
        f.close()
        return False
    else:
        f.close()
        return True

roledefault = discord.Color.default()
rolered = discord.Color.red()
roleorange = discord.Color.orange()
roleyellow = discord.Color.gold()
rolegreen = discord.Color.green()
roleblue = discord.Color.dark_blue()
rolepurple = discord.Color.purple()
# The Fun Stuff

@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    check_all_perms()
    serverstats()


@client.event
async def on_message(message):
    if message.content == 'ok':
        await client.add_reaction(message, '🇩')
        await client.add_reaction(message, '🇮')
        await client.add_reaction(message, '🇪')
    if message.content == '!yes':
        await client.send_message(message.channel,'I want to die')
    if message.content == '!rainbowrole':
        if hasadmin(message) == False:
            await client.send_message(message.channel, "**" + str(message.author) + "**, you do not have permissions to use this command!")
        else:
            try:
                rbrlnum = random.randint(1,1000)
                rbrlname = 'RainbowRole' + str(rbrlnum)
                await client.create_role(server=message.server,name=rbrlname)
                rbrl = None
                for role in message.server.roles:
                    if str(role.name) == "new role":
                        rbrl = role.id
                        await client.edit_role(server=message.server,role=role,color=rolered)
                        await client.edit_role(server=message.server,role=role,mentionable=True)
            except Exception as e:
                await client.send_message(message.channel, "**" + str(
                    message.author) + "**, BonesBot does not have permissions to preform this!")
                print(e)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(exc_traceback.tb_lineno)
            rbfn = 'serverstats/bonesbot-' + message.server.id + '-rb.txt'
            f = open(rbfn,"r")
            if len(str(f.readlines())) > 5:
                await client.send_message(message.channel, "**" + str(message.author) + "**, there already exists a Rainbow Role!")
                for role in message.server.roles:
                    if str(role.name) == "new role":
                        await client.delete_role(server=message.server,role=role)
                f.close()
            else:
                f.close()
                f = open(rbfn,"a")
                f.write(str(rbrl))
                f.close()
                await client.send_message(message.channel, "**" + str(message.author) + "**, role created!")
    if '!anysizelist' in message.content:
        whilemetdone = False
        alslist = []
        def check(msg):
            return msg.content.startswith('!anysizelist')
        message = await client.wait_for_message(author=message.author,check=check)
        retvalmain = message.content[len('!anysizelist'):].strip()
        if retvalmain == "":
            await client.send_message(message.channel,"**" + str(message.author) + "**, no arguments provided!")
        elif is_int(retvalmain) == False:
            await client.send_message(message.channel,"**" + str(message.author) + "**, invalid argument!")
        else:
            await client.send_message(message.channel,'**' + str(message.author) + "**, using list of " + retvalmain + ".")
            while whilemetdone == False:
                await client.send_message(message.channel,'Enter the PLACEMENT of a demon in that list with *!demon-anysizelist (demon)*. Say \'Done\' when done.')
                def check(msg):
                    return msg.content.startswith('!demon-anysizelist')
                message = await client.wait_for_message(author=message.author,check=check)
                retval = message.content[len('!demon-anysizelist'):].strip()
                if retval == "":
                    await client.send_message(message.channel, "**" + str(message.author) + "**, no demon specified!")
                elif is_int(retval) == False and retval != 'Done':
                    await client.send_message(message.channel, "**" + str(message.author) + "**, invalid demon!")
                elif retval == 'Done':
                    whilemetdone = True
                elif is_int(retval) == True:
                    if int(retval) <= 0 or int(retval) > int(retvalmain):
                        await client.send_message(message.channel, "**" + str(message.author) + "**, demon out of range!")
                    elif retval in alslist:
                        await client.send_message(message.channel,"**" + str(message.author) + "**, demon already entered!")
                    else:
                        alslist.append(retval)
                        await client.send_message(message.channel,"Added demon with placement #" + retval + '.')
            await client.send_message(message.channel,"Results for **" + str(message.author) + "\'s** list of " + retvalmain + ":")
            endscr = psc(float(retvalmain),alslist)
            await client.send_message(message.channel,"You have a score of " + str(endscr) + '!')
    if '!bonesbothelp' in message.content:
        await client.send_message(message.channel,boneshelp)
    if '!createtoplist' in message.content:
        if hasadmin(message) == False:
            await client.send_message(message.channel, "**" + str(message.author) + "**, you do not have permissions to use this command!")
        else:
            servfn = 'serverstats/bonesbot-' + message.server.id + '-hasdl.txt'
            f = open(servfn,'r')
            def check(msg):
                return msg.content.startswith('!createtoplist')
            message = await client.wait_for_message(author=message.author,check=check)
            retvalmain = message.content[len('!createtoplist'):].strip()
            if retvalmain == '':
                await client.send_message(message.channel, "**" + str(message.author) + "**, no argument provided!")
            elif is_int(retvalmain) == False:
                await client.send_message(message.channel, "**" + str(message.author) + "**, invalid argument!")
            elif int(retvalmain) < 5:
                await client.send_message(message.channel, "**" + str(message.author) + "**, the list needs to be greater than 5!")
            else:
                retvalmain = int(retvalmain)
                if 'yes' in f.readlines():
                    await client.send_message(message.channel, "**" + str(
                        message.author) + "**, a demon list already exists on this server!")
                else:
                    try:
                        f.close()
                        f = open(servfn, 'a')
                        f.write('yes')
                        f.close()
                        nametoplist = 'top-' + str(retvalmain) + '-server-list'
                        nametopplayers = 'top-' + str(retvalmain) + '-players-list'
                        nametopsubmit = 'submit-for-top-' + str(retvalmain)
                        potoplist = discord.PermissionOverwrite()
                        potoplist.send_messages = False
                        potoplist.send_tts_messages = False
                        potoplist.manage_messages = False
                        potoplist.embed_links = False
                        potoplist.attach_files = False
                        potoplist.mention_everyone = False
                        potoplist.external_emojis = False
                        potoplist.add_reactions = False
                        await client.create_channel(server=message.server,name=nametoplist)
                        await client.edit_channel_permissions(name=nametoplist,role="@everyone",overwrite=potoplist)
                        await client.create_channel(server=message.server,name=nametopplayers)
                        await client.edit_channel_permissions(name=nametopplayers,role="@everyone", overwrite=potoplist)
                        await client.create_channel(server=message.server,name=nametopsubmit)
                    except Exception as e:
                        await client.send_message(message.channel,"**" + str(message.author) + "**, BonesBot does not have permissions to preform this!")
                        print(e)
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print(exc_traceback.tb_lineno)
                    servdlname = 'serverstats/bonesbot-' + message.server.id + '-demonlist.txt'
                    f = open(servdlname,'a')
                    dlist = []
                    for i in range(1,retvalmain):
                        dlist.append(str(i) + '. ')
                    plistnames = []
                    plistscores = []
                    f.write(str(dlist) + '\n' + str(plistnames) + '\n' + str(plistscores))
                    f.close()
                    f = open(servdlname,'r')
                    dlmsg = '**Top ' + str(retvalmain) + '** Demon List:\n'
                    identoplist = None
                    identopplayers = None
                    identopsubmit = None
                    for i in dlist:
                        dlmsg = dlmsg + str(i) + '\n'
                    for i in client.get_all_channels():
                        if i.name == nametoplist:
                            identoplist = i.id
                        elif i.name == nametopplayers:
                            identopplayers = i.id
                        elif i.name == nametopsubmit:
                            identopsubmit = i.id
                    await client.send_message(id=identoplist,content=dlmsg)
                    await client.send_message(id=identopplayers,content='**Top ' + str(retvalmain) + '** Player\'s List:\n')
                    await client.send_message(id=identopsubmit,content='Here you can submit entries for the **Top ' + str(retvalmain) + '** List!')
                    await client.pin_message(content='Here you can submit entries for the **Top ' + str(retvalmain) + '** List!')
                    await client.send_message(message.channel,'Created Top ' + str(retvalmain) + ' List!')
    if message.content == '!activaterb':
        if rbcycle(message) == True:
            rbacstop = False
            print('Rainbow Role activated for Server \"' + str(message.server.name) + '\"')
            rbfn = 'serverstats/bonesbot-' + message.server.id + '-rb.txt'
            f = open(rbfn, "r")
            rbid = str(f.readlines())
            rbid = rbid.translate(trtlrunpass)
            for role in message.server.roles:
                if role.id == rbid:
                    f.close()
                    while rbcycle(message) == True and rbacstop == False:
                        try:
                            if role.color == rolered:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=roleorange)
                            if role.color == roleorange:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=roleyellow)
                            if role.color == roleyellow:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=rolegreen)
                            if role.color == rolegreen:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=roleblue)
                            if role.color == roleblue:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=rolepurple)
                            if role.color == rolepurple:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=rolered)
                            if role.color == roledefault:
                                time.sleep(0.3)
                                await client.edit_role(server=message.server, role=role, color=rolered)
                        except:
                            await client.send_message(message.server,"BonesBot does not have permissions to activate the rainbow effect (This is usually when the role is higher ranking than BonesBot)")
                            rbacstop = True
client.run(runpass)