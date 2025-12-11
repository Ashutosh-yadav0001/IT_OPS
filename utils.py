#!/usr/bin/env python3
"""
Utility script for common Azure Graph API operations.

This script provides a command-line interface for common operations.
"""

import argparse
import logging
import sys
import json
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def cmd_list_users(client: GraphAPIClient, args):
    """List users command."""
    logger = logging.getLogger(__name__)
    
    users = client.list_users(
        top=args.limit,
        select=["displayName", "userPrincipalName", "mail", "jobTitle"]
    )
    
    if users and 'value' in users:
        logger.info(f"Found {len(users['value'])} users:")
        for user in users['value']:
            print(f"\n{user.get('displayName', 'N/A')}")
            print(f"  UPN: {user.get('userPrincipalName', 'N/A')}")
            print(f"  Email: {user.get('mail', 'N/A')}")
            print(f"  Title: {user.get('jobTitle', 'N/A')}")
    else:
        logger.error("Failed to retrieve users")


def cmd_get_user(client: GraphAPIClient, args):
    """Get user details command."""
    logger = logging.getLogger(__name__)
    
    user = client.get_user(args.user_id)
    
    if user:
        print(json.dumps(user, indent=2))
    else:
        logger.error(f"User {args.user_id} not found")


def cmd_list_groups(client: GraphAPIClient, args):
    """List groups command."""
    logger = logging.getLogger(__name__)
    
    groups = client.list_groups(
        top=args.limit,
        select=["displayName", "description", "mail"]
    )
    
    if groups and 'value' in groups:
        logger.info(f"Found {len(groups['value'])} groups:")
        for group in groups['value']:
            print(f"\n{group.get('displayName', 'N/A')}")
            print(f"  Description: {group.get('description', 'N/A')}")
            print(f"  Email: {group.get('mail', 'N/A')}")
            print(f"  ID: {group.get('id', 'N/A')}")
    else:
        logger.error("Failed to retrieve groups")


def cmd_list_group_members(client: GraphAPIClient, args):
    """List group members command."""
    logger = logging.getLogger(__name__)
    
    members = client.list_group_members(args.group_id)
    
    if members and 'value' in members:
        logger.info(f"Found {len(members['value'])} members:")
        for member in members['value']:
            print(f"  - {member.get('displayName', 'N/A')} ({member.get('userPrincipalName', member.get('id'))})")
    else:
        logger.error("Failed to retrieve group members")


def cmd_org_info(client: GraphAPIClient, args):
    """Get organization info command."""
    logger = logging.getLogger(__name__)
    
    org = client.get_organization()
    
    if org and 'value' in org:
        print(json.dumps(org['value'], indent=2))
    else:
        logger.error("Failed to retrieve organization information")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Azure Graph API Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List users command
    parser_list_users = subparsers.add_parser('list-users', help='List users')
    parser_list_users.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='Maximum number of users to return (default: 10)'
    )
    
    # Get user command
    parser_get_user = subparsers.add_parser('get-user', help='Get user details')
    parser_get_user.add_argument('user_id', help='User ID or UPN')
    
    # List groups command
    parser_list_groups = subparsers.add_parser('list-groups', help='List groups')
    parser_list_groups.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='Maximum number of groups to return (default: 10)'
    )
    
    # List group members command
    parser_group_members = subparsers.add_parser('list-group-members', help='List group members')
    parser_group_members.add_argument('group_id', help='Group ID')
    
    # Organization info command
    parser_org = subparsers.add_parser('org-info', help='Get organization information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Authenticate
        logger.info("Authenticating with Azure AD...")
        auth = AzureGraphAuth(config_path=args.config)
        token = auth.authenticate_client_credentials()
        
        if not token:
            logger.error("Authentication failed")
            sys.exit(1)
        
        logger.info("Authentication successful")
        
        # Create client
        client = GraphAPIClient(auth)
        
        # Execute command
        if args.command == 'list-users':
            cmd_list_users(client, args)
        elif args.command == 'get-user':
            cmd_get_user(client, args)
        elif args.command == 'list-groups':
            cmd_list_groups(client, args)
        elif args.command == 'list-group-members':
            cmd_list_group_members(client, args)
        elif args.command == 'org-info':
            cmd_org_info(client, args)
        
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {args.config}")
        logger.error("Please copy config.template.json to config.json and fill in your credentials")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
