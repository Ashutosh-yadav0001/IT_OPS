#!/usr/bin/env python3
"""
Advanced example script for Azure Graph API operations.

This script demonstrates:
1. User management (create, update, get)
2. Group management
3. Group membership operations
4. Error handling
"""

import logging
import sys
import json
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def example_user_operations(client: GraphAPIClient, logger: logging.Logger):
    """
    Demonstrate user management operations.
    
    Note: This is for demonstration. Actual user creation requires
    appropriate permissions and valid domain.
    """
    logger.info("\n=== USER OPERATIONS EXAMPLE ===")
    
    # Get a specific user (replace with actual UPN or ID)
    user_id = "user@yourdomain.com"  # Replace with actual user
    logger.info(f"Getting user: {user_id}")
    
    user = client.get_user(user_id, select=["displayName", "userPrincipalName", "jobTitle", "department"])
    
    if user:
        logger.info(f"Found user: {json.dumps(user, indent=2)}")
    else:
        logger.warning(f"User {user_id} not found or access denied")
    
    # Example: Update user (uncomment and modify to use)
    # update_data = {
    #     "jobTitle": "Senior Developer"
    # }
    # result = client.update_user(user_id, update_data)
    # if result:
    #     logger.info("User updated successfully")


def example_group_operations(client: GraphAPIClient, logger: logging.Logger):
    """Demonstrate group management operations."""
    logger.info("\n=== GROUP OPERATIONS EXAMPLE ===")
    
    # List all groups with detailed information
    logger.info("Listing groups with details...")
    groups = client.list_groups(top=10, select=["displayName", "description", "mail", "groupTypes"])
    
    if groups and 'value' in groups:
        logger.info(f"Found {len(groups['value'])} groups:")
        for group in groups['value']:
            logger.info(f"\nGroup: {group.get('displayName')}")
            logger.info(f"  Description: {group.get('description', 'N/A')}")
            logger.info(f"  Email: {group.get('mail', 'N/A')}")
            logger.info(f"  Types: {group.get('groupTypes', [])}")
            
            # Get members of the first group as an example
            if groups['value'].index(group) == 0:
                group_id = group.get('id')
                logger.info(f"\n  Listing members of group: {group.get('displayName')}")
                members = client.list_group_members(group_id)
                
                if members and 'value' in members:
                    logger.info(f"  Found {len(members['value'])} members")
                    for member in members['value'][:5]:  # Show first 5
                        logger.info(f"    - {member.get('displayName', 'N/A')}")
    else:
        logger.warning("No groups found or error occurred")


def example_application_operations(client: GraphAPIClient, logger: logging.Logger):
    """Demonstrate application listing."""
    logger.info("\n=== APPLICATION OPERATIONS EXAMPLE ===")
    
    logger.info("Listing registered applications...")
    apps = client.list_applications(top=5)
    
    if apps and 'value' in apps:
        logger.info(f"Found {len(apps['value'])} applications:")
        for app in apps['value']:
            logger.info(f"\nApplication: {app.get('displayName')}")
            logger.info(f"  App ID: {app.get('appId')}")
            logger.info(f"  Object ID: {app.get('id')}")
    else:
        logger.warning("No applications found or error occurred")


def example_custom_query(client: GraphAPIClient, logger: logging.Logger):
    """Demonstrate custom Graph API queries."""
    logger.info("\n=== CUSTOM QUERY EXAMPLE ===")
    
    # Example: Get all users who are guest users
    logger.info("Querying for guest users...")
    params = {
        "$filter": "userType eq 'Guest'",
        "$select": "displayName,userPrincipalName,userType",
        "$top": "5"
    }
    
    guests = client.get("/users", params=params)
    
    if guests and 'value' in guests:
        logger.info(f"Found {len(guests['value'])} guest users:")
        for guest in guests['value']:
            logger.info(f"  - {guest.get('displayName')} ({guest.get('userPrincipalName')})")
    else:
        logger.warning("No guest users found or query failed")


def main():
    """Main execution function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Authenticate
        logger.info("Authenticating with Azure AD...")
        auth = AzureGraphAuth(config_path="config.json")
        token = auth.authenticate_client_credentials()
        
        if not token:
            logger.error("Authentication failed. Please check your credentials.")
            sys.exit(1)
        
        logger.info("Authentication successful!")
        
        # Create client
        client = GraphAPIClient(auth)
        
        # Run examples
        example_user_operations(client, logger)
        example_group_operations(client, logger)
        example_application_operations(client, logger)
        example_custom_query(client, logger)
        
        logger.info("\n=== All examples completed ===")
        
    except FileNotFoundError:
        logger.error("Configuration file not found. Please copy config.template.json to config.json and fill in your credentials.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
