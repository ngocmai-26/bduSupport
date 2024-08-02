import random
from django.core.cache import cache

class OtpService():
    def generate_otp(self, length: int, purpose: str, email: str) -> str:
        cache.delete_many(cache.keys(f"{purpose}:account:{email}:otp:*"))

        otp = str(random.randint(10**length, 10**(length + 1) - 1))
        cache.set(f"{purpose}:account:{email}:otp:{otp}", email, 3600)

        return otp
    
    def verify_otp(self, purpose: str, email: str, otp: str) -> bool:
        return cache.get(f"{purpose}:account:{email}:otp:{otp}", None) is not None