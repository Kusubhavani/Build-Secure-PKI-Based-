from totp_utils import generate_totp_code, verify_totp_code

seed = "7595316af4533c80ed5b9e1d8a33fb9e51f2bfb4c678f4d48b9c170a7823a072"

code = generate_totp_code(seed)
print("TOTP:", code)

print("Valid?", verify_totp_code(seed, code))
