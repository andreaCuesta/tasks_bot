import database


class User:
    def __init__(self, name, last_name, chat_id):
        self.name = name
        self.last_name = last_name
        self.chat_id = chat_id

    def register(self):
        user_data = (self.name, self.last_name, self.chat_id)
        database.insert_user(user_data)

    @staticmethod
    def get_user_by_chat_id(chat_id):
        user = database.get_user_by_chat_id(chat_id)

        if user is None:
            return user
        else:
            new_user = User(user[1], user[2], user[3])

            return new_user
