import base64
import re
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def safe_b64decode(data):
    """Bulletproof base64 decode"""
    cleaned = re.sub(b'[^A-Za-z0-9+/=]', b'', data.encode('ascii'))
    return base64.b64decode(cleaned)

private_key = serialization.load_pem_private_key(open('student_private.pem', 'rb').read(), password=None)
encrypted_data = open('encrypted_seed.b64', 'r').read().strip()

print(f"📊 Input: {len(encrypted_data)} chars")
print(f"🔍 Decoding base64...")
ciphertext = safe_b64decode(encrypted_data)
print(f"✅ Ciphertext: {len(ciphertext)} bytes")

print("🔓 Decrypting...")
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

seed = plaintext.decode('utf-8').strip()
print(f"🎉 SEED: {seed}")
print(f"📏 Length: {len(seed)} chars")

if len(seed) == 64 and seed.isalnum():
    with open('seed.txt', 'w') as f:
        f.write(seed)
    print("💾 SAVED to seed.txt")
    print("✅ SUCCESS!")
else:
    print("⚠️  WARNING: Seed format unexpected")
