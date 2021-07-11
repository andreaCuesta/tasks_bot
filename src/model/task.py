import DB.database as database

class Task:
    def __init__(self, link, user_id, id=None, status="pendiente", grade=None):
        self.id = id
        self.link = link
        self.status = status
        self.grade = grade
        self.user_id = user_id

    def register(self):
        task_data = (self.link, self.status, self.grade, self.user_id)
        return database.insert_task(task_data)

    def edit(self, new_link):
        database.edit_task(self.id, new_link)
        return self.get_by_id_and_user(self.id, self.user_id)

    def delete(self):
        database.delete_task(self.id)

    @staticmethod
    def get_by_user_and_link(user_id, link):
        return database.get_task_by_user_and_link(user_id, link)

    @staticmethod
    def get_by_id_and_user(task_id, user_id):
        task = database.get_task_by_id_and_user(task_id, user_id)

        if task is None:
            return task
        else:
            new_task = Task(id=task[0], link=task[1], status=task[2], grade=task[3], user_id=task[4])

            return new_task

    @staticmethod
    def list_by_user(user_id):
        tasks = database.list_tasks_by_user(user_id)

        user_tasks = []

        for task in tasks:
            new_task = Task(id=task[0], link=task[1], status=task[2], grade=task[3], user_id=task[4])
            user_tasks.append(new_task)

        return user_tasks
