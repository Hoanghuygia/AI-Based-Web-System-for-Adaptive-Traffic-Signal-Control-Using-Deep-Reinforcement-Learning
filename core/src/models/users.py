from .rwmodels import RWModel
from pydantic import AnyUrl

from .dbmodel import DBModelMixin
from ..core.security import verify_password, generate_salt, get_password_hash

class UserBase(RWModel):
    username: str
    image: AnyUrl | None = None
    
class UserInDB(DBModelMixin, UserBase):
    salt: str = "" # we need to use salt to generate random string because if we do not use salt then the two passwords which the same will have the same hased string
    hashed_password: str = ""
    
    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)
    
    def change_password(self, password: str): 
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)
    
class User(UserBase):
    token: str
    
class UserInResponse(RWModel):
    user: User
    
class UserInLogin(RWModel):
    username: str
    password: str
    
