class AbstractUser:
    pid: int
    user_id: string
    password = models.CharField(max_length=64)
    nickname:
    isSeller: bool
