#!/usr/bin/env python3
import datetime
import os
import sys

import yaml


KEYDO_FILE = os.getenv("KEYDO_FILE", "keydo.yaml")
DEFAULT_CONTEXT = 'default'

def print_help():
    print("KeyDo Usage")
    print("a/action/actions: manage actions")
    print("p/project/projects: manage projects")
    print("s/stats: show stats")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    else:
        main_cmd = sys.argv[1]
        if not os.path.exists(KEYDO_FILE):
            with open(KEYDO_FILE, 'w') as f:
                f.write('actions: {}\nprojects: {}\nreference: {}')
        with open(KEYDO_FILE, 'r') as f:
            config = yaml.safe_load(f)
        if main_cmd in ['s', 'stats']:
            print(f"{len(config['actions'])} next actions")
            print(f"{len(config['projects'])} projects")
            print(f"{len(config['reference'])} reference items")
        elif main_cmd in ['p', 'project', 'projects']:
            if len(sys.argv) < 3:
                print("Projects subcommands:")
                print("n/new: new project")
                print("l/list: list projects")
            else:
                subcommand = sys.argv[2]
                if subcommand in ['l', 'list']:
                    for project in config['projects'].values():
                        print(f"✅ P{project['id']}) {project['name']} - {project['updated']}")
                elif subcommand in ['n','new']:
                    id = 1
                    while id in config['projects']:
                        id += 1
                    name = input("Enter name of project: ")
                    outcome = input("Describe desired outcome: ")
                    last_update = datetime.datetime.now().strftime("%Y-%m-%d")
                    config['projects'][id] = {
                        'id': id,
                        'name': name,
                        'outcome': outcome,
                        'updated': last_update,
                        'action': None,
                    }
                    with open(KEYDO_FILE, 'w') as f:
                        yaml.safe_dump(config, f)
        elif main_cmd in ['a', 'action', 'actions']:
            if len(sys.argv) < 3:
                print("Actions subcommands:")
                print("n/new: new action")
                print("l/list: list actions")
            else:
                subcommand = sys.argv[2]
                if subcommand in ['n', 'new']:
                    id = 1
                    all_actions = {}
                    for context in config['actions'].values():
                        for action in context.values():
                            all_actions[action['id']] = action
                    while id in all_actions:
                        id += 1
                    name = input("Enter action: ")
                    context = input("Enter context: ")
                    if len(context) < 1:
                        context = DEFAULT_CONTEXT
                    if context not in config['actions']:
                        config['actions'][context] = {}
                    print("Projects:")
                    for project in config['projects'].values():
                        print(f"{project['id']}) {project['name']}")
                    project = input("Enter project id or leave blank: ")
                    config['actions'][context][id] = {
                        'id': id,
                        'name': name,
                        'project': project,
                        'context': context,
                    }
                    with open(KEYDO_FILE, 'w') as f:
                        yaml.safe_dump(config, f)
                elif subcommand in ['l', 'list']:
                    print("Next Actions")
                    print()
                    for context in config['actions'].keys():
                        print(f"Context: {context} ({len(config['actions'][context])})")
                        for action in config['actions'][context].values():
                            if action['project']:
                                project = config['projects'][int(action['project'])]
                            else:
                                project = {'name': ''}
                            print(f"✅ A{action['id']}) {action['name']} ({project['name']})")
                        print()
