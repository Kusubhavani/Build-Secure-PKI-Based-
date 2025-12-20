import base64
import re
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def safe_b64decode(data: str) -> bytes:
    """Safely decode base64 with cleaning and auto-padding."""
    # Convert to bytes and clean: remove non-base64 chars, whitespace
    if isinstance(data, str):
        data = data.encode('ascii')
    data = re.sub(rb'[^A-Za-z0-9+/=]', b'', data.strip())
    
    # Add padding (0-3 '=' chars)
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    
    try:
        return base64.b64decode(data)
    except Exception:
        raise ValueError("Invalid base64 data after cleaning")

def decrypt_seed(encrypted_seed_b64: str, private_key):
    """Decrypt RSA-OAEP encrypted seed with proper error handling."""
    try:
        # Decode base64 safely
        ciphertext = safe_b64decode(encrypted_seed_b64)
        print(f"Decoded ciphertext length: {len(ciphertext)} bytes")  # Debug
        
        # Decrypt with OAEP padding
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decode UTF-8 (handle potential BOM or encoding issues)
        seed = plaintext.decode("utf-8").strip()
        
        # Validate TOTP seed: 64 hex chars (32 bytes)
        if len(seed) != 64 or not re.match(r'^[0-9a-fA-F]{64}$', seed):
            raise ValueError(f"Invalid seed format: {seed[:16]}... (len={len(seed)})")
        
        return seed
        
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")

def load_private_key(path="student_private.pem"):
    """Load PEM private key."""
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(), 
                password=None
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key not found: {path}")

if __name__ == "__main__":
    try:
        private_key = load_private_key("student_private.pem")
        print("✅ Private key loaded")
        
        # Read encrypted seed file
        with open("encrypted_seed.b64", "r", encoding="utf-8") as f:
            encrypted_seed = f.read()
        
        print(f"Raw encrypted_seed length: {len(encrypted_seed)}")
        print(f"Last 50 chars: {encrypted_seed[-50:]}")
        
        # Decrypt and save
        seed = decrypt_seed(encrypted_seed, private_key)
        
        with open("seed.txt", "w") as f:
            f.write(seed)
        
        print("✅ Decrypted seed saved to seed.txt:")
        print(seed)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nDebug checklist:")
        print("- student_private.pem exists?")
        print("- encrypted_seed.b64 exists and contains valid base64?")
        print("- Run: python decrypt_seed.py")
