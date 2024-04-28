#!/usr/bin/env python3
import datetime
import os
import sys

import yaml


KEYDO_FILE = os.getenv("KEYDO_FILE", "keydo.yaml")

def print_help():
    print("KeyDo Usage")
    print("s/stats: show stats")
    print("p/projects: manage projects")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    else:
        main_cmd = sys.argv[1]
        if not os.path.exists(KEYDO_FILE):
            with open(KEYDO_FILE, 'w') as f:
                f.write('next_actions: []\nprojects: []\nreference: []')
        with open(KEYDO_FILE, 'r') as f:
            config = yaml.safe_load(f)
        if main_cmd in ['s', 'stats']:
            print(f"{len(config['next_actions'])} next actions")
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
                    for project in config['projects']:
                        print(f"✅⚠ {project['name']} - {project['updated']}")
                elif subcommand in ['n','new']:
                    id = 1
                    name = input("Enter name of project: ")
                    last_update = datetime.datetime.now().strftime("%Y-%m-%d")
                    config['projects'].append({
                        'id': id,
                        'name': name,
                        'updated': last_update
                    })
                    with open(KEYDO_FILE, 'w') as f:
                        yaml.safe_dump(config, f)
