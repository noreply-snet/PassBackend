from dateutil import tz
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def convert_utc_to_ist(utc_time):
    # Define timezones
    utc_zone = tz.tzutc()
    ist_zone = tz.gettz('Asia/Kolkata')
    
    # Convert UTC time to IST
    ist_time = utc_time.replace(tzinfo=utc_zone).astimezone(ist_zone)
    return ist_time