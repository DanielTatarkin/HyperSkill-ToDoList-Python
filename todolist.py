from datetime import datetime, timedelta
from sql_util import SqlSession


class ToDoList:
    PROMPT = "1) Today's tasks\n" \
             "2) Week's tasks\n" \
             "3) All tasks\n" \
             "4) Add task\n" \
             "0) Exit"
    TODAY_TASKS = 1
    WEEK_TASKS = 2
    ALL_TASKS = 3
    ADD_TASK = 4
    EXIT = 0

    def __init__(self):
        self.SQL = SqlSession()

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

    def shutdown(self):
        print("\nBye!")
        exit(0)

    def incorrect_input(self):
        print("Incorrect input, try again\n")
        self.print_prompt()

    def print_prompt(self):
        fun_choices = {
            self.TODAY_TASKS: self.list_tasks,
            self.WEEK_TASKS: self.list_tasks,
            self.ALL_TASKS: self.list_tasks,
            self.ADD_TASK: self.add_task,
            self.EXIT: self.shutdown
        }
        print(self.PROMPT)
        try:
            user_choice = int(input("> "))
        except ValueError:
            print("Please enter a digit 0-4")
            self.print_prompt()
            return
        if user_choice in range(self.TODAY_TASKS, self.ALL_TASKS + 1):
            fun_choices.get(user_choice, self.incorrect_input)(user_choice)
        else:
            fun_choices.get(user_choice, self.incorrect_input)()


def main():
    app = ToDoList()
    while True:
        app.print_prompt()


if __name__ == '__main__':
    main()
