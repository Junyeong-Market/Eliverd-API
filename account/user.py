from account.models import User


class AbstractUser:
    model: User
    pid: int
    user_id: str
    nickname: str
    is_seller: bool


class AnonymousUser(AbstractUser):
    pid = -1
    user_id = ""
    nickname = ""
    isSeller = ""


class NormalUser(AbstractUser):
    def __init__(self, model):
        self.model = model
        self.pid = model.pid
        self.user_id = model.user_id
        self.nickname = model.nickname
        self.is_seller = model.is_seller
