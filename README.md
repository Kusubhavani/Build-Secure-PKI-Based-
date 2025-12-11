PKI-Based Two-Factor Authentication (2FA)

This project implements a simple Two-Factor Authentication (2FA) system using:

✔ Public-Key Cryptography (RSA) ✔ One-Time Password (OTP) ✔ Digital Signatures ✔ Python cryptography library

Project Files File Description generate_keys.py Generates RSA private & public keys generate_otp.py Creates OTP & signs it using private key authenticate.py Verifies OTP & signature using public key student_private.pem Student's private key student_public.pem Student's public key otp.txt Stores generated OTP otp_signature.bin Digital signature of OTP

Generate Keys → Creates RSA private/public key pair

Generate OTP → Random 6-digit OTP → Signed using private key → Stored in otp.txt & otp_signature.bin

Authenticate User → Enter OTP → Verify OTP + digital signature using public key → Shows Authentication Successful or Failed

Commands Used python generate_keys.py python generate_otp.py python authenticate.py

Technologies Used

Python 3

Cryptography Library (RSA, SHA-256, Signatures)

Git & GitHub

Linux-like CLI (Git Bash)
