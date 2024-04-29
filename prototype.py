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

def manage_actions(args, parser):
    config = get_config()
    if args.subcommand in ['n', 'new']:
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
        set_config(config)
    elif args.subcommand in ['l', 'list']:
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
    else:
        parser.print_help()


def manage_projects(args, parser):
    config = get_config()
    if args.subcommand in ['l', 'list']:
        for project in config['projects'].values():
            print(f"✅ P{project['id']}) {project['name']} - {project['updated']}")
    elif args.subcommand in ['n','new']:
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
        set_config(config)
    else:
        parser.print_help()


def show_stats(args, parser):
    config = get_config()
    print(f"{len(config['actions'])} next actions")
    print(f"{len(config['projects'])} projects")
    print(f"{len(config['reference'])} reference items")

def main():
    if not os.path.exists(KEYDO_FILE):
        print(f"KeyDo file not found at {KEYDO_FILE}, creating...")
        with open(KEYDO_FILE, 'w') as f:
            f.write('actions: {}\nprojects: {}\nreference: {}')

    parser = argparse.ArgumentParser(description="KeyDo CLI tool")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Subparser for managing actions
    action_parser = subparsers.add_parser("a", aliases=["action"], help="Manage actions")
    action_subparsers = action_parser.add_subparsers(title="Subcommand", dest="subcommand")
    action_subparsers.add_parser('l', aliases=['list'], help='List actions')
    action_subparsers.add_parser('n', aliases=['new'], help='Create new action')

    # Subparser for managing projects
    project_parser = subparsers.add_parser("p", aliases=["project"], help="Manage projects")
    project_subparsers = project_parser.add_subparsers(title="Subcommand", dest="subcommand")
    project_subparsers.add_parser('l', aliases=['list'], help='List projects')
    project_subparsers.add_parser('n', aliases=['new'], help='Create new project')

    # Subparser for showing stats
    stats_parser = subparsers.add_parser("s", aliases=["stats"], help="Show stats")

    args = parser.parse_args()

    if args.command in ['a', 'action']:
        manage_actions(args, action_parser)
    elif args.command in ['p', 'project']:
        manage_projects(args, project_parser)
    elif args.command in ['s', 'stats']:
        show_stats(args, stats_parser)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
