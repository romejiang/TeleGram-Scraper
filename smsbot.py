#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
    {re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
    {re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

                version : 3.1
    youtube.com/channel/UCnknCgg_3pVXS27ThLpw3xQ
            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        
        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        fname = sys.argv[2] if len(sys.argv) >= 3 else ""
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1] send sms by user ID\n[2] send sms by username ")
        mode = int(input(gr+"Input : "+re))
        
        message = input(gr+"[+] Enter Your Message : "+re)
        n=0
        openz=False
        if fname == "":
            openz=True
        
        for user in users:
            n += 1
            if (not openz) and (user['id'] == int(fname)):
                openz=True
            if not openz:
                print(gr+"[+] Skip:", user['name'],user['id'])
                continue
            SLEEP_TIME = random.randrange(150, 180)
            if n % 5 == 0:
                SLEEP_TIME = random.randrange(5, 8) * 60
                print(gr+"[+] 5 = Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Sending Message to:",n, user['name'],user['id'])
                client.send_message(receiver, message.format(user['name']))
            except PeerFloodError:
                print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                SLEEP_TIME = random.randrange(15,25) * 60
                print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
                client.connect()
                if not client.is_user_authorized():
                    client.send_code_request(phone)
                    os.system('clear')
                    main.banner()
                    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
                # sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Trying to continue...")
            finally:
                print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
        client.disconnect()
        print("Done. Message sent to all users.")



main.send_sms()
