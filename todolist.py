from datetime import datetime, timedelta
from sql_util import SqlSession


class ToDoList:
    PROMPT = "1) Today's tasks\n" \
             "2) Week's tasks\n" \
             "3) All tasks\n" \
             "4) Missed tasks\n" \
             "5) Add task\n" \
             "6) Delete task\n" \
             "0) Exit"
    TODAY_TASKS = 1
    WEEK_TASKS = 2
    ALL_TASKS = 3
    MISSED_TASKS = 4
    ADD_TASK = 5
    DELETE_TASK = 6
    EXIT = 0

    def __init__(self):
        self.SQL = SqlSession()
        self.actions = {
            self.TODAY_TASKS: self.list_tasks,
            self.WEEK_TASKS: self.list_tasks,
            self.ALL_TASKS: self.list_tasks,
            self.MISSED_TASKS: self.list_tasks,
            self.ADD_TASK: self.add_task,
            self.DELETE_TASK: self.delete_task,
            self.EXIT: self.shutdown
        }

    def list_tasks(self, choice):
        today = datetime.today()

        if choice == self.TODAY_TASKS:
            print(f"\nToday {today.strftime('%d %b')}:")
            rows_list = self.SQL.get_today_tasks()
            if len(rows_list) == 0:
                print("Nothing to do!")
            else:
                for i, task in enumerate(rows_list, start=1):
                    print(i, task, sep='. ')
            print("")

        elif choice == self.WEEK_TASKS:
            date_list = [today.date() + timedelta(days=x) for x in range(7)]
            for date in date_list:
                print(f'\n{datetime.strftime(date, "%A %d %b:")}')
                tasks = self.SQL.get_date_task(date)
                if len(tasks) > 0:
                    for i, task in enumerate(tasks, start=1):
                        print(i, task, sep='. ')
                else:
                    print("Nothing to do!")
            print("")

        elif choice == self.ALL_TASKS:
            print("\nAll tasks:")
            rows_list = self.SQL.get_all_tasks()
            if len(rows_list) == 0:
                print("Nothing to do!")
            else:
                for i, task in enumerate(rows_list, start=1):
                    print(i, task, datetime.strftime(task.deadline, "%d %b"), sep='. ')
            print("")

        elif choice == self.MISSED_TASKS:
            print("\nMissed tasks:")
            rows_list = self.SQL.get_missed_tasks()
            if len(rows_list) == 0:
                print("Nothing is missed!")
            else:
                for i, task in enumerate(rows_list, start=1):
                    print(i, task, datetime.strftime(task.deadline, "%d %b"), sep='. ')
            print("")

    def add_task(self):
        print("\nEnter task")
        task = input(">")
        print("Enter deadline")
        deadline = input(">")
        try:
            if not deadline: deadline = str(datetime.today().date())
            date = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("Error, bad date format, ex: YYYY-mm-dd")
            self.add_task()
            return
        self.SQL.add_task(task, date)
        print("The task has been added!\n")

    def delete_task(self):
        missed_tasks = self.SQL.get_missed_tasks() + self.SQL.get_today_tasks()
        if len(missed_tasks) == 0:
            print("\nNo missed tasks or today's tasks\n")
            return
        else:
            print("\nChoose the number of the task you want to delete:")

            for i, task in enumerate(missed_tasks, start=1):
                print(i, task, datetime.strftime(task.deadline, "%d %b"), sep='. ')

            for _ in range(10):
                try:
                    user_pick = int(input(">"))
                except ValueError:
                    print("Error, bad entry, please enter a task number")
                    continue
                finally:
                    break
            self.SQL.delete_task(missed_tasks[user_pick - 1])
            print("The task has been deleted!\n")

    @staticmethod
    def shutdown():
        print("\nBye!")
        exit(0)

    def incorrect_input(self):
        print("Incorrect input, try again\n")
        self.print_prompt()

    def print_prompt(self):
        print(self.PROMPT)
        try:
            user_choice = int(input("> "))
        except ValueError:
            print("Please enter a digit 0-4")
            self.print_prompt()
            return
        if user_choice in [self.TODAY_TASKS, self.WEEK_TASKS, self.ALL_TASKS, self.MISSED_TASKS]:
            self.actions.get(user_choice, self.incorrect_input)(user_choice)
        else:
            self.actions.get(user_choice, self.incorrect_input)()


def main():
    app = ToDoList()
    while True:
        app.print_prompt()


if __name__ == '__main__':
    main()
