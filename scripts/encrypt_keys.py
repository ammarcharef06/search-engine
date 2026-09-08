from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import json, os, secrets

keys = {
    "SHODAN_KEY": "xxx",
    "CENSYS_ID": "xxx",
    "CENSYS_SECRET": "xxx",
    # ... باقي المفاتيح
}

# نستخدم المفتاح المشتق من كلمات المرور الثلاث (يُولد مرة واحدة)
key = secrets.token_bytes(32)
nonce = secrets.token_bytes(12)
cipher = ChaCha20Poly1305(key)
encrypted = cipher.encrypt(nonce, json.dumps(keys).encode(), None)

with open("api_keys.enc", "wb") as f:
    f.write(nonce + encrypted)

print("تم تشفير المفاتيح. احتفظ بالمفتاح:", key.hex())