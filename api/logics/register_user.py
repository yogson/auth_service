from api.logics.local_user import LocalUser, get_password_hash
from models.user import UserInDB


class LocalUserRegister(LocalUser):

    def register(self):
        if not self.users_db.get_user_by_name(self.username):
            self.user = UserInDB(username=self.username, hashed_password=get_password_hash(self.password))
            self.users_db.save_user(user=self.user)
            return self
