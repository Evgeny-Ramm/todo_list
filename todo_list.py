#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# todo_list.py
# Список задач с цветным выводом и синхронизацией с рабочим столом.

import argparse
import os
from colorama import init, Fore, Style

init(autoreset=True)

TASKS_FILE = "tasks.txt"
DESKTOP_TASKS = os.path.expanduser("~/Рабочий стол/tasks.txt")

def load_tasks():
    tasks = []
    if os.path.exists(DESKTOP_TASKS):
        with open(DESKTOP_TASKS, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    tasks.append(line)
    return tasks

def save_tasks(tasks):
    with open(DESKTOP_TASKS, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

def add_task(tasks, task):
    tasks.append(task)
    save_tasks(tasks)
    print(f"задача добавлена: {task}")

def list_tasks(tasks):
    if not tasks:
        print("список задач пуст")
        return
    print("список задач:")
    for i, task in enumerate(tasks, start=1):
        if task.startswith("[x]"):
            print(f"{Fore.GREEN}{i}. {task}{Style.RESET_ALL}")
        else:
            print(f"{i}. {task}")

def delete_task(tasks, index):
    if not tasks:
        print("список задач пуст")
        return
    if index < 1 or index > len(tasks):
        print("неверный номер задачи")
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"задача удалена: {removed}")

def complete_task(tasks, index):
    if not tasks:
        print("список задач пуст")
        return
    if index < 1 or index > len(tasks):
        print("неверный номер задачи")
        return
    task = tasks[index - 1]
    if not task.startswith("[x]"):
        tasks[index - 1] = "[x] " + task
        save_tasks(tasks)
        print(f"задача отмечена как выполненная: {task}")
    else:
        print("задача уже выполнена")

def main():
    parser = argparse.ArgumentParser(description="список задач (todo)")
    parser.add_argument("command", choices=["add", "list", "delete", "complete", "done"], help="команда")
    parser.add_argument("arg", nargs="?", help="аргумент (текст задачи или номер)")
    args = parser.parse_args()

    tasks = load_tasks()

    if args.command == "add":
        if not args.arg:
            print("укажите задачу: todo add 'сделать что-то'")
            return
        add_task(tasks, args.arg)

    elif args.command == "list":
        list_tasks(tasks)

    elif args.command == "delete":
        if not args.arg:
            print("укажите номер задачи для удаления")
            return
        try:
            index = int(args.arg)
            delete_task(tasks, index)
        except ValueError:
            print("номер должен быть числом")

    elif args.command == "complete" or args.command == "done":
        if not args.arg:
            print("укажите номер задачи для отметки выполненной")
            return
        try:
            index = int(args.arg)
            complete_task(tasks, index)
        except ValueError:
            print("номер должен быть числом")

if __name__ == "__main__":
    main()
