from src.models.rwmodels import RWModel

class TokenPayLoad(RWModel):
    username: str = ""
    
class RefreshTokenRequest(RWModel):
    refresh_token: str
    
class TokenResponse(RWModel):
    access_token: str
    refresh_token: str