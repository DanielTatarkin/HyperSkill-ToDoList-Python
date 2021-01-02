from sql_util import SqlSession

SQL = SqlSession()


def main():
    while True:
        print_prompt()


def list_tasks():
    rows_li = SQL.query()
    print("\nToday:")
    if len(rows_li) == 0:
        print("Nothing to do!")
    else:
        for num, task in enumerate(rows_li, start=1):
            print(f"{num}. {task}")
    print("")


def add_task():
    print("\nEnter task")
    task = input(">")
    SQL.add_task(task)
    print("The task has been added!\n")


def print_prompt():
    print("1) Today's tasks\n"
          "2) Add task\n"
          "0) Exit")
    choice = int(input("> "))

    if choice == 1:
        list_tasks()
    elif choice == 2:
        add_task()
    elif choice == 0:
        print("\nBye!")
        exit(0)
    else:
        print("Incorrect input, try again")
        print_prompt()


if __name__ == '__main__':
    main()
