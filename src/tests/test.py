from pathlib import Path

from dao.infile_user_dao import FileUsersDAO

data = Path("users.json")


users = FileUsersDAO(file_obj=data)

print(users.get_user_by_name("user"))
