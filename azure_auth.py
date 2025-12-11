"""
Azure Graph API Authentication Module

This module handles authentication with Azure AD and Microsoft Graph API
using the MSAL (Microsoft Authentication Library) for Python.
"""

import json
import logging
from typing import Optional, Dict, Any
import msal


class AzureGraphAuth:
    """
    Handles authentication with Azure AD for Microsoft Graph API access.
    
    Supports:
    - Client credentials flow (app-only authentication)
    - Future: User authentication flows
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the authentication handler.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.app = None
        self.token = None
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise
    
    def authenticate_client_credentials(self) -> Optional[str]:
        """
        Authenticate using client credentials flow (app-only).
        
        This method is suitable for daemon/service applications that run
        without user interaction.
        
        Returns:
            Access token if successful, None otherwise
        """
        try:
            azure_config = self.config.get('azure', {})
            
            # Create a confidential client application
            self.app = msal.ConfidentialClientApplication(
                azure_config['client_id'],
                authority=azure_config['authority'],
                client_credential=azure_config['client_secret']
            )
            
            # Acquire token for Graph API
            result = self.app.acquire_token_for_client(
                scopes=azure_config['scope']
            )
            
            if "access_token" in result:
                self.token = result['access_token']
                self.logger.info("Successfully authenticated with Azure AD")
                return self.token
            else:
                error = result.get("error", "Unknown error")
                error_desc = result.get("error_description", "No description")
                self.logger.error(f"Authentication failed: {error} - {error_desc}")
                return None
                
        except KeyError as e:
            self.logger.error(f"Missing configuration key: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return None
    
    def get_token(self) -> Optional[str]:
        """
        Get the current access token.
        
        Returns:
            Current access token or None if not authenticated
        """
        return self.token
    
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.token is not None
