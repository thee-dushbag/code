from models import DB_KEY, User
from aiohttp import web
from sqlalchemy.orm import Session

async def add_user(req: web.Request, name: str, password: str, email: str):
    print("Adding User With Data:")
    print(f"\tName:    {name}")
    print(f"\tEmail:    {email}")
    print(f"\tPassword: {password}")
    if not all((name, password, email)): return
    session = req.app[DB_KEY]
    user = User(name=name, password=password, email=email)
    session.add(user)
    try:
        session.commit()
    except Exception:
        session.rollback()
    else:
        return user.user_id

async def get_user(req: web.Request, user_id: int):
    session = req.app[DB_KEY]
    try:
        user = session.query(User).where(User.user_id == user_id).one()
    except Exception:
        return
    else:
        return user
    
async def del_user(req: web.Request, user_id: int):
    session:Session = req.app[DB_KEY]
    try:
        user = await get_user(req, user_id)
        if not user:
            raise Exception
        session.delete(user)
        session.commit()
    except Exception:
        session.rollback()
    else:
        return True