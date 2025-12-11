"""
IT_OPS - Azure Graph API Integration

A Python package for working with Microsoft Graph API to manage Azure AD resources.

Main Components:
- azure_auth: Authentication with Azure AD
- graph_client: Graph API client for operations
- example_basic: Basic usage examples
- example_advanced: Advanced usage examples
- utils: Command-line utilities

For more information, see README.md
"""

__version__ = "1.0.0"
__author__ = "IT_OPS Team"
__description__ = "Azure Graph API Integration for IT Operations"

# Make key classes available at package level
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient

__all__ = ["AzureGraphAuth", "GraphAPIClient"]
