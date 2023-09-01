from aiohttp import web
from typing import Any
from pydantic import EmailStr, EmailError
import wtforms as wtf, attrs

@attrs.define
class User:
    name: str
    email: str
    password: str

    def __hash__(self) -> int:
        return hash(self.name)

@attrs.define
class Users:
    users: list[User] = attrs.field(factory=list)
    def get_user(self, name: str):
        for user in self.users:
            if user.name == name:
                return user
    def add_user(self, user: User):
        if self.get_user(user.name):
            return None
        self.users.append(user)
        return user

users = Users()

class FormValidationError(Exception):
    def __init__(self, field_name: str, field_value: Any) -> None:
        self.name = field_name
        self.value = field_value

class LoginForm(wtf.Form):
    name = wtf.StringField('name')
    password = wtf.StringField('password')
    
    def validate_name(self, name):
        print(f"Validating name: {name.data}")
        if name.data is None:
            raise FormValidationError('name', name.data)
    
    def validate_password(self, password):
        print(f"Validating password: {password.data}")
        if password.data is None:
            raise FormValidationError('password', password.data)

class SignupForm(LoginForm):
    email = wtf.StringField('email')

    def validate_email(self, email):
        print(f"Validating email: {email.data}")
        if email.data is None:
            raise FormValidationError('email', email.data)
        validator = EmailStr()
        try:
            validator.validate(email.data)
        except EmailError as e:
            raise FormValidationError('email', email.data)

async def signup(req: web.Request):
    data = await req.post()
    form = SignupForm(formdata=data)
    try:
        form.validate()
    except FormValidationError as e:
        return web.json_response({'status': 'Unsuccessful Signup', 'error_value': f'field {e.name} cannot be {e.value}'}, status=401)
    else:
        user = User(**form.data)
        users.add_user(user)
        return web.json_response({'status': 'Successful Signup'})

async def login(req: web.Request):
    data = await req.post()
    form = LoginForm(formdata=data)
    try:
        form.validate()
    except FormValidationError as e:
        return web.json_response({'status': 'Unsuccessful Signup', 'error_value': f'field {e.name} cannot be {e.value}'}, status=401)
    else:
        user = User(**form.data, email='')
        suser = users.get_user(user.name)
        if suser is None:
            return web.json_response({'status': 'User Not Found', 'user': user.name})
        if user.password == suser.password:
            return web.json_response({'status': 'Succeccful Login', 'user': user.name})
        else:
            return web.json_response({'status': 'Wrong Password', 'user': user.name})

routes = [
    web.post('/signup', signup),
    web.post('/login', login)
]

async def app_factory() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app