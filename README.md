# RSA Breaker 
is a python script that automates all the steps and calculations to solve the TryHackme.com lab entitled: [**Breaking RSA**](https://tryhackme.com/jr/breakrsa)


`git clone https://github.com/kali-mx/RSA_breaker.git` 

`python3 RSA_breaker.py`

https://github.com/kali-mx/RSA_breaker/assets/76034874/4e40d6c2-00ab-4f39-bd7d-0740a2aaa5be


This Python script is designed to break RSA encryption by factorizing the RSA modulus to retrieve the private key components, enabling unauthorized SSH access to a server by reconstructing its SSH private key.

## Features

- **Banner Display**: Utilizes `pyfiglet` to display "RSA Breaker" as a stylized banner.
- **Modular Inverse Calculation**: Contains a function to compute the modular inverse, critical for RSA decryption.
- **RSA Modulus Factorization**: Implements an algorithm to factorize the RSA modulus into its prime factors (p and q).
- **Private Exponent (d) Calculation**: Calculates the RSA private exponent using the factorized primes.
- **SSH Private Key Reconstruction**: Generates an RSA private key from the calculated components and serializes it into PEM format.

## Workflow

1. **Initial Setup**: Clears the screen and displays the program banner.
2. **Fetch and Save Public Key**: Prompts for an IP address, fetches the public SSH key from the server, and saves it locally.
3. **Public Key Analysis**: Determines the bit size of the public key.
4. **Modulus Extraction and Conversion**: Extracts the modulus from the public key, converting it to decimal format.
5. **Factorization and Calculation**: Factorizes the modulus to find primes (p and q), then calculates the private exponent (d).
6. **Private Key Generation**: Generates and saves the corresponding SSH private key in PEM format.
7. **SSH Access Attempt**: Attempts to log into the server using the generated private key to execute commands.

## Usage

To use this script, you'll need to have Python 3 installed along with the `colorama`, `gmpy2`, `pyfiglet`, and `cryptography` libraries. 


