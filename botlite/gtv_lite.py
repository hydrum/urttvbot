import socket
import string
import urllib
from time import ctime
from time import sleep

IP="irc.quakenet.org"
PORT=6667
NICK="GTV-Bot-LITE"
IDENT="GTV-Bot"
REALNAME="GTV-Bot"
text=""
channel="#urt-tv"
OWNER="~gost0r@Gost0r.users.quakenet.org"
admins="~Gost0r"

qauth = "GTV-Bot xxx"

pubchan = "#urt-tv"
privchan = "xxx"
altchan = "xxx"

dbfile = "gtv_lite.txt"


stop = 0
result = 0
spamnum = 0
tsec = 0

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( IP, PORT ) )
irc.send ( 'USER  ' + IDENT + ' ' + IDENT + ' bla : ' + REALNAME + '\n' )
irc.send ( 'NICK ' + NICK + '\n')


while True:
    try:
        text = irc.recv(4096)
        print text
        data = text.split()

        if len(data) <= 0:
            data = ['', '']

        if data[1] == "513":
            irc.send('PONG ' + data[8] + '\n')

        if "PING" in text:
            irc.send('PONG ' + data[1] + '\n')
            
        if "MOTD" in text:
            irc.send ( 'PRIVMSG Q@CServe.quakenet.org :AUTH ' + qauth + '\n')
            sleep(1)
            irc.send ( 'MODE ' + NICK + ' :+x \n')
            irc.send ( 'JOIN ' + pubchan + '\n')
            irc.send ( 'JOIN ' + privchan + '\n')
            irc.send ( 'JOIN ' + altchan + '\n')
            
        if "PRIVMSG" in text:
            getnick = data[0].split("!")
            nick = getnick[0].replace(":","")
            nick = nick.replace("\'","`")
            
            if data[3] == ":!die":
                host = getnick[1]
                if host == OWNER:
                    irc.send('QUIT\n')
                    close


            if data[3] == ":!gtv":
                channel = data[2]
                if pubchan in data[2]:
                    if len(data) <= 4:
                        irc.send('PRIVMSG ' + channel + ' :GTV parameter missing: try !gtv help\n')
                        
                    elif data[4] == "upcoming":
                        fileHandle = open(dbfile)
                        read = fileHandle.read()
                        fileHandle.close()
                        read = read.split("\n")
                        found = False
                        for i in range(0,len(read)):
                            gtv1 = read[i].split(" ")
                            if gtv1[0] == "PUB":
                                if gtv1[7] == "0":
                                    server = "NOT SET"
                                else:
                                    server = gtv1[7]
                                if gtv1[8] == "0":
                                    stream = "NOT SET"
                                else:
                                    stream = gtv1[8]
                                irc.send('PRIVMSG ' + channel + ' :' + gtv1[5] + ' ' + gtv1[6] + ':  ' + gtv1[1] + ' vs ' + gtv1[2] + ' @ ' + gtv1[3] + ' ' + gtv1[4] + ' - Server: ' + server + ' - Stream: ' + stream + '\n')
                                found = True
                        if found == False:
                                irc.send('PRIVMSG ' + channel + ' :No upcoming GTV\n')
                                
                    elif data[4] == "last":
                        fileHandle = open(dbfile)
                        read = fileHandle.read()
                        fileHandle.close()
                        read = read.split("\n")
                        found = 0
                        i = len(read) - 1
                        while i >= 0:
                            gtv1 = read[i].split(" ")
                            if gtv1[0] == "DONE":
                                if gtv1[9] == "0":
                                    score = "NOT SET"
                                else:
                                    score = gtv1[9]
                                if gtv1[10] == "0":
                                    demo = "NOT SET"
                                else:
                                    demo = gtv1[10]
                                irc.send('PRIVMSG ' + channel + ' :' + gtv1[5] + ' ' + gtv1[6] + ':  ' + gtv1[1] + ' vs ' + gtv1[2] + ' - Score: ' + score + ' - Demo: ' + demo + '\n')
                                found = found + 1
                            if found == 3:
                                break
                            i = i - 1
                        if found == 0:
                            irc.send('PRIVMSG ' + channel + ' :No passed GTV\n')
                                
                            

                if (data[2] == privchan) or (data[2] == altchan):
                    if len(data) <= 4:
                        pass
                    
                    elif data[4] == "add":
                        if len(data) == 11:
                            addline = 'PRIV ' + str(data[5]) + ' ' + str(data[6]) + ' ' + str(data[7]) + ' ' + str(data[8]) + ' ' + str(data[9]) + ' ' + str(data[10]) + ' 0 0 0 0'
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) == 0:
                                lines.append(addline)
                            else:
                                lines.append('\n' + addline)
                            swrite = ''
                            f = open(dbfile, 'w')
                            for i in range(0,len(lines)):
                                swrite = swrite + lines[i]
                            f.write(swrite)
                            f.close()
                            irc.send('PRIVMSG ' + channel + ' :GTV match added\n')
                        else:
                            irc.send('PRIVMSG ' + channel + ' :GTV add parameter missing: !gtv add <TeamA> <TeamB> <date> <time> <league> <gametype>\n')

                    elif data[4] == "delete":
                        if len(data) == 6:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[int(data[5])] =  'DEL ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + changeline[7] + ' ' + changeline[8] + ' ' + changeline[9] + ' ' + changeline[10]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV match deleted\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')

                    elif data[4] == "done":
                        if len(data) == 8:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[int(data[5])] =  'DONE ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + changeline[7] + ' ' + changeline[8] + ' ' + data[6] + ' ' + data[7]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV match done\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')

                    elif data[4] == "list":
                        fileHandle = open(dbfile)
                        read = fileHandle.read()
                        fileHandle.close()
                        read = read.split("\n")
                        found = False
                        for i in range(0,len(read)):
                            gtv1 = read[i].split(" ")
                            if gtv1[0] == "PUB":
                                if gtv1[7] == "0":
                                    server = "NOT SET"
                                else:
                                    server = gtv1[7]
                                if gtv1[8] == "0":
                                    stream = "NOT SET"
                                else:
                                    stream = gtv1[8]
                                irc.send('PRIVMSG ' + channel + ' :#' + str(i) + ': ' + gtv1[1] + ' vs ' + gtv1[2] + ' @ ' + gtv1[3] + ' ' + gtv1[4] + ' - Server: ' + server + ' - Stream: ' + stream + '\n')
                                found = True
                        if found == False:
                            irc.send('PRIVMSG ' + channel + ' :No upcoming GTV\n')

                    elif data[4] == "free":
                        fileHandle = open(dbfile)
                        read = fileHandle.read()
                        fileHandle.close()
                        read = read.split("\n")
                        found = False
                        for i in range(0,len(read)):
                            gtv1 = read[i].split(" ")
                            if gtv1[0] == "PRIV":
                                if gtv1[7] == "0":
                                    server= "NOT SET"
                                else:
                                    server = gtv1[7]
                                if gtv1[8] == "0":
                                    stream = "NOT SET"
                                else:
                                    stream = gtv1[8]
                                irc.send('PRIVMSG ' + channel + ' :#' + str(i) + ': ' + gtv1[1] + ' vs ' + gtv1[2] + ' @ ' + gtv1[3] + ' ' + gtv1[4] + ' - Server: ' + server + ' - Stream: ' + stream + '\n')
                                found = True
                        if found == False:
                            irc.send('PRIVMSG ' + channel + ' :No upcoming GTV\n')

                    elif data[4] == "take":
                        if len(data) == 7:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[int(data[5])] =  'PUB ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + data[6] + ' ' + changeline[8] + ' ' + changeline[9] + ' ' + changeline[10]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV match taken\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')
                        else:
                            irc.send('PRIVMSG ' + channel + ' :GTV take: !gtv take <id> <server>\n')

                    elif data[4] == "remove":
                        if len(data) == 6:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[data[5]] =  'PRIV ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + changeline[7] + ' ' + changeline[8] + ' ' + changeline[9] + ' ' + changeline[10]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV match removed\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')
                        else:
                            irc.send('PRIVMSG ' + channel + ' :GTV take: !gtv remove <id>\n')

                    elif data[4] == "streamadd":
                        if len(data) == 7:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[int(data[5])] =  changeline[0] + ' ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + changeline[7] + ' ' + data[6] + ' ' + changeline[9] + ' ' + changeline[10]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV stream added\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')
                        else:
                            irc.send('PRIVMSG ' + channel + ' :GTV take: !gtv streamadd <id> <link>\n')

                    elif data[4] == "streamremove":
                        if len(data) == 6:
                            f = open(dbfile, 'r')
                            lines = f.readlines()
                            f.close()
                            if len(lines) > int(data[5]):
                                changeline = lines[int(data[5])].split(" ")
                                lines[int(data[5])] = changeline[0] + ' ' + changeline[1] + ' ' + changeline[2] + ' ' + changeline[3] + ' ' + changeline[4] + ' ' + changeline[5] + ' ' + changeline[6] + ' ' + changeline[7] + ' 0 ' + changeline[9] + ' ' + changeline[10]
                                swrite = ''
                                f = open(dbfile, 'w')
                                for i in range(0,len(lines)):
                                    swrite = swrite + lines[i]
                                f.write(swrite)
                                f.close()
                                irc.send('PRIVMSG ' + channel + ' :GTV stream removed\n')
                            else:
                                irc.send('PRIVMSG ' + channel + ' :GTV ID not found\n')
                        else:
                            irc.send('PRIVMSG ' + channel + ' :GTV take: !gtv streamremove <id>\n')
                            
                    elif data[4] == "servers":
                        irc.send('PRIVMSG ' + channel + ' :GTV #1 IP: gtv1.urt-tv.org:27973 - Admin: xxx - Camera: xxx\n')
                        irc.send('PRIVMSG ' + channel + ' :GTV #2 IP: gtv1.urt-tv.org:27970 - Admin: xxx - Camera: xxx\n')

    except socket.error:
        continue
