from .rwmodels import RWModel
from pydantic import AnyUrl, Field, field_validator
import re
from typing import Optional

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
    # refresh_token: str
    refresh_token: Optional[str] = None
    
class UserInResponse(RWModel):
    user: User
    
class UserInLogin(RWModel):
    username: str
    password: str = Field(..., min_length=10)
    
    # @field_validator('password')
    # def validate_password(cls, password: str) -> str:
    #     """
    #     Validate that password must:
    #     - Be at least 8 characters
    #     - Contain at least one uppercase letter
    #     - Contain at least one lowercase letter
    #     - Contain at least one number
    #     - Contain at least one special character
    #     """
    #     error_message = ("Password must be at least 10 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character")
        
    #     if not re.search(r'[A-Z]', password):
    #         raise ValueError(error_message)
        
    #     if not re.search(r'[a-z]', password):
    #         raise ValueError(error_message)
        
    #     if not re.search(r'\d', password):
    #         raise ValueError(error_message)
        
    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #         raise ValueError(error_message)
        
    #     return password
    
