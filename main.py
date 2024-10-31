import argparse
from datetime import datetime
import json

parser = argparse.ArgumentParser(description="Task CLI")
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser('add', help='Add a new task')
add_parser.add_argument('task_id', type=int, help='ID of the task to add')
add_parser.add_argument('task_description', type=str, help='Description of the task')

update_parser = subparsers.add_parser('update', help='Update a task')
update_parser.add_argument('task_id', type=int, help='ID of the task to delete')
update_parser.add_argument('task_description', type=str, help='Updated description of the task')

delete_parser = subparsers.add_parser('delete', help='Delete a task')
delete_parser.add_argument('task_id', type=int, help='ID of the task to delete')

mark_parser = subparsers.add_parser('mark', help='Change the status of the task')
mark_subparsers = mark_parser.add_subparsers(dest="mark_command")

mark_in_progress_parser = mark_subparsers.add_parser('in-progress', help='Mark a task as in progress')
mark_in_progress_parser.add_argument('task_id', type=int, help='ID of the task to mark as in progress')

mark_done_parser = mark_subparsers.add_parser('done', help='Mark a task as done')
mark_done_parser.add_argument('task_id', type=int, help='ID of the task to mark as done')

list_parser = subparsers.add_parser('list', help='List tasks')
list_subparsers = list_parser.add_subparsers(dest='list_command')

list_done_parser = list_subparsers.add_parser('done', help='List done tasks')
list_todo_parser = list_subparsers.add_parser('todo', help='List todo tasks')
list_in_progress_parser = list_subparsers.add_parser('in-progress', help='List in progress tasks')

args = parser.parse_args()


class Task:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.status = 'todo'
        self.createdAt = (datetime.now()).timestamp()
        self.updatedAt = (datetime.now()).timestamp()
    
    
    def update_description(self, description):
        self.description = description
        self.updatedAt = (datetime.now()).timestamp()
    
    
    def change_status(self, status):
        self.status = status
        self.updatedAt = (datetime.now()).timestamp()
        
        
    def to_dict(self):
        return self.__dict__
    
    
    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


file = open('data.json', 'r+')

try:
    tasks = json.load(file)
except json.JSONDecodeError:
    tasks = []
    print("File doesnt exists, or was corrupted. Making a new file")

def get_task(id):
    for el in tasks:
        if el['id'] == id:
            return el, tasks.index(el)
    return None, None


def show_task(task, status='all'):
    if task['status'] == status or status == 'all':
        for key, value in task.items():
            if key == 'createdAt':
                print(f'{key} = {datetime.fromtimestamp(value)}')
            elif key == 'updatedAt':
                print(f'{key} = {datetime.fromtimestamp(value)}')        
            else:
                print(f'{key} = {value}')
        print('------------------------------------------')
                
                
match args.command:
    case 'add':
        task, _ = get_task(args.task_id)
        if task is None:
            tasks.append(Task(args.task_id, args.task_description).to_dict())
        else:
            print('Task with this id already exists')
    case 'update':
        task, index = get_task(args.task_id)
        if task is None:
            print('Task doest exists')
        else:
            tasks[index]['description'] = args.description
    case 'delete':
        task, index = get_task(args.task_id)
        if task is None:
            print('Nothing to delete')
        else:
            tasks.pop(index)
    case 'mark':
        task, index = get_task(args.task_id)
        if task is None:
            print('Task doest exists')
        else:
            tasks[index]['status'] = args.mark_command
    case 'list':
        match args.list_command:
            case None:
                for el in tasks:
                    show_task(el)
            case 'done':
                for el in tasks:
                    show_task(el, 'done')
            case 'todo':
                for el in tasks:
                    show_task(el, 'todo')
            case 'in-progress':
                for el in tasks:
                    show_task(el, 'in-progress')

file.seek(0)
file.truncate()

json.dump(tasks, file, indent=4)
        
file.close()