import database


class Task:
    def __init__(self, link, user_id, id=None, state="on hold", grade=None):
        self.id = id
        self.link = link
        self.state = state
        self.grade = grade
        self.user_id = user_id

    def register(self):
        task_data = (self.link, self.state, self.grade, self.user_id)
        return database.insert_task(task_data)

    @staticmethod
    def get_task_by_user_and_link(user_id, link):
        return database.get_task_by_user_and_link(user_id, link)

    @staticmethod
    def get_task_by_id_and_user(task_id, user_id):
        task = database.get_task_by_id_and_user(task_id, user_id)
        print(task)

        if task is None:
            return task
        else:
            new_task = Task(id=task[0], link=task[1], state=task[2], grade=task[3], user_id=task[4])

            return new_task
