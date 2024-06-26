#!/usr/bin/env python3
import argparse
import datetime
import os

import yaml


KEYDO_FILE = os.getenv("KEYDO_FILE", "keydo.yaml")
DEFAULT_CONTEXT = 'default'

def get_config() -> dict:
    with open(KEYDO_FILE, 'r') as f:
        config = yaml.safe_load(f)
    return config

def set_config(config: dict):
    with open(KEYDO_FILE, 'w') as f:
        yaml.safe_dump(config, f)

def id_exists(collection, id):
    for item in collection:
        if item['id'] == id:
            return True
    return False

def manage_actions(args, parser):
    config = get_config()
    if args.subcommand in ['n', 'new']:
        id = 1
        while id_exists(config['actions'], id):
            id += 1
        name = input("Enter action: ")
        context = input("Enter context: ")
        if len(context) < 1:
            context = DEFAULT_CONTEXT
        print("Projects:")
        for project in config['projects']:
            print(f"{project['id']}) {project['name']}")
        project = input("Enter project id or leave blank: ")
        config['actions'].append({
            'id': id,
            'name': name,
            'project': project,
            'context': context,
        })
        set_config(config)
    elif args.subcommand in ['d', 'delete']:
        print("Delete action")
        id_to_delete = int(input("Enter action id: ").upper().replace('A', ''))
        config = get_config()
        actions_filtered = []
        for action in config['actions']:
            if action['id'] != id_to_delete:
                actions_filtered.append(action)
        config['actions'] = actions_filtered
        set_config(config)
    else:
        print("Next Actions")
        print()
        contexts = set()
        for action in config['actions']:
            contexts.add(action['context'])
        for context in contexts:
            matches = [x for x in config['actions'] if x['context'] == context]
            print(f"Context: {context}")
            print()
            print("ID\tName\t\tProject")
            print("----------------------------------")
            for action in matches:
                project = {'name': ''}
                if action['project']:
                    for p in config['projects']:
                        if p['id'] == int(action['project']):
                            project = p
                print(f"A{action['id']}\t{action['name']}\t{project['name']}")
            print()
            print()


def manage_projects(args, parser):
    config = get_config()
    if args.subcommand in ['n','new']:
        id = 1
        while id_exists(config['actions'], id):
            id += 1
        name = input("Enter name of project: ")
        outcome = input("Describe desired outcome: ")
        category = input("Enter category: ")
        last_update = datetime.datetime.now().strftime("%Y-%m-%d")
        config['projects'].append({
            'id': id,
            'name': name,
            'outcome': outcome,
            'updated': last_update,
            'category': category,
        })
        set_config(config)
    elif args.subcommand in ['d', 'delete']:
        print("Delete project")
        id_to_delete = int(input("Enter project id: ").upper().replace('P', ''))
        config = get_config()
        projects_filtered = []
        for project in config['projects']:
            if project['id'] != id_to_delete:
                projects_filtered.append(project)
        config['projects'] = projects_filtered
        set_config(config)
    else:
        print("ID\tProject\t\tCategory\tUpdated")
        print("--------------------------------------------------")
        for project in config['projects']:
            print(f"P{project['id']}\t{project['name']}\t{project['category']}\t{project['updated']}")


def show_stats(args, parser):
    config = get_config()
    print(f"{len(config['actions'])} next actions")
    print(f"{len(config['projects'])} projects")
    print(f"{len(config['reference'])} reference items")

def run_review(args, parser):
    config = get_config()
    print("Weekly Review")
    print("-------------")
    print("Action Review")
    for action in config['actions']:
        print(action)
        user_in = None
        while user_in not in ['y','n']:
            user_in = input("Delete this action? (y/n) ")
        if user_in == 'y':
            pass
            print("removing")
        else:
            pass
            print("keeping")
    print()
    print("Project Review")
    for project in config['projects']:
        print(project)
        user_in = None
        while user_in not in ['y','n']:
            user_in = input("Delete this project? (y/n) ")
        if user_in == 'y':
            pass
            print("removing")
        else:
            pass
            print("keeping")
        ## TODO set next action if not exists
        # TODO: either way, update last updated date

def main():
    if not os.path.exists(KEYDO_FILE):
        print(f"KeyDo file not found at {KEYDO_FILE}, creating...")
        with open(KEYDO_FILE, 'w') as f:
            f.write('actions: []\nprojects: []\nreference: []')

    parser = argparse.ArgumentParser(description="KeyDo CLI tool")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Subparser for managing actions
    action_parser = subparsers.add_parser("a", aliases=["action", "actions"], help="Manage actions")
    action_subparsers = action_parser.add_subparsers(title="Subcommand", dest="subcommand")
    action_subparsers.add_parser('n', aliases=['new'], help='Create new action')
    action_subparsers.add_parser('d', aliases=['delete'], help='Delete action')

    # Subparser for managing projects
    project_parser = subparsers.add_parser("p", aliases=["project", "projects"], help="Manage projects")
    project_subparsers = project_parser.add_subparsers(title="Subcommand", dest="subcommand")
    project_subparsers.add_parser('n', aliases=['new'], help='Create new project')
    project_subparsers.add_parser('d', aliases=['delete'], help='Delete project')

    # Subparser for showing stats
    stats_parser = subparsers.add_parser("s", aliases=["stat", "stats"], help="Show stats")

    # Subparser for weekly review
    review_parser = subparsers.add_parser("r", aliases=["review"], help="Review GTD")

    args = parser.parse_args()

    if args.command in ['a', 'action', 'actions']:
        manage_actions(args, action_parser)
    elif args.command in ['p', 'project', 'projects']:
        manage_projects(args, project_parser)
    elif args.command in ['s', 'stat', 'stats']:
        show_stats(args, stats_parser)
    elif args.command in ['r', 'review']:
        run_review(args, review_parser)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
