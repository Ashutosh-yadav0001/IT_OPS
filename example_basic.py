#!/usr/bin/env python3
"""
Example script demonstrating basic usage of Azure Graph API client.

This script shows how to:
1. Authenticate with Azure AD
2. List users in the organization
3. Get user details
4. List groups
5. Get organization information
"""

import logging
import sys
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main execution function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Step 1: Authenticate
        logger.info("Authenticating with Azure AD...")
        auth = AzureGraphAuth(config_path="config.json")
        token = auth.authenticate_client_credentials()
        
        if not token:
            logger.error("Authentication failed. Please check your credentials.")
            sys.exit(1)
        
        logger.info("Authentication successful!")
        
        # Step 2: Create Graph API client
        client = GraphAPIClient(auth)
        
        # Step 3: List users
        logger.info("\n--- Listing Users ---")
        users_response = client.list_users(top=5, select=["displayName", "userPrincipalName", "mail"])
        
        if users_response and 'value' in users_response:
            for user in users_response['value']:
                logger.info(f"User: {user.get('displayName')} ({user.get('userPrincipalName')})")
        else:
            logger.warning("No users found or error occurred")
        
        # Step 4: List groups
        logger.info("\n--- Listing Groups ---")
        groups_response = client.list_groups(top=5, select=["displayName", "mail"])
        
        if groups_response and 'value' in groups_response:
            for group in groups_response['value']:
                logger.info(f"Group: {group.get('displayName')} ({group.get('mail', 'N/A')})")
        else:
            logger.warning("No groups found or error occurred")
        
        # Step 5: Get organization info
        logger.info("\n--- Organization Information ---")
        org_response = client.get_organization()
        
        if org_response and 'value' in org_response:
            for org in org_response['value']:
                logger.info(f"Organization: {org.get('displayName')}")
                logger.info(f"Tenant ID: {org.get('id')}")
        else:
            logger.warning("Could not retrieve organization information")
        
        logger.info("\n--- Example completed successfully ---")
        
    except FileNotFoundError:
        logger.error("Configuration file not found. Please copy config.template.json to config.json and fill in your credentials.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
