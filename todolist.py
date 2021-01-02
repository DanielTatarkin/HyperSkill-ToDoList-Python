from sql_util import SqlSession

SQL = SqlSession()
PROMPT = "1) Today's tasks\n" \
         "2) Add task\n" \
         "0) Exit"


def main():
    while True:
        print_prompt()


def list_tasks():
    rows_li = SQL.get_tasks()
    print("\nToday:")
    if len(rows_li) == 0:
        print("Nothing to do!")
    else:
        for task in rows_li:
            print(task)
    print("")


def add_task():
    print("\nEnter task")
    task = input(">")
    SQL.add_task(task)
    print("The task has been added!\n")


def shutdown():
    print("\nBye!")
    exit(0)


def incorrect_input():
    print("Incorrect input, try again\n")
    print_prompt()


def print_prompt():
    print(PROMPT)
    choice = input("> ")
    fun_choices = {'1': list_tasks, '2': add_task, '0': shutdown}
    fun_choices.get(choice, incorrect_input)()


if __name__ == '__main__':
    main()
