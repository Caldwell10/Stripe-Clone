import bcrypt
from models import Transaction_Logs 

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def save_transaction_log(db, direction: str, url: str, payload: str, status_code: int):
    log = Transaction_Logs(
        direction=direction,
        url=url,
        payload=payload,
        status_code=status_code
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

