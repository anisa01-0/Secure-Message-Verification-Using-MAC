import hmac
import hashlib

def generate_mac(message: str, key: str) -> str:
    """Generate HMAC-SHA256 for the given message and key"""
    key_bytes = key.encode('utf-8')
    msg_bytes = message.encode('utf-8')
    mac = hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()
    return mac

def verify_mac(message: str, key: str, received_mac: str) -> bool:
    """Verify if the received MAC matches the generated MAC"""
    expected_mac = generate_mac(message, key)
    return hmac.compare_digest(expected_mac, received_mac)