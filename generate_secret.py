import secrets

# Generate a random 16-byte secret key, which will produce a 32-character hexadecimal string
secret_key = secrets.token_hex(16)

print("Generated Secret Key:", secret_key)
