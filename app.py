from src.tasks_api import close_task, create_task, create_subtask, get_task


if __name__ == "__main__":
    # create_task("Zrobić zakupy", "czekolada\nkurwa gruszka\nitd", 5)
    # close_task(1)
    # add_subtask(1, "krowa", "dupa", 1)
    print(get_task(1).id)
