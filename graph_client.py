"""
Microsoft Graph API Client Module

This module provides a client wrapper for interacting with Microsoft Graph API,
making it easier to perform common operations on Azure AD resources.
"""

import logging
import requests
from typing import Optional, Dict, Any, List
from azure_auth import AzureGraphAuth


class GraphAPIClient:
    """
    Client for interacting with Microsoft Graph API.
    
    Provides methods for common operations:
    - User management
    - Group management
    - Application management
    - General API requests
    """
    
    def __init__(self, auth: AzureGraphAuth, use_beta: bool = False):
        """
        Initialize the Graph API client.
        
        Args:
            auth: Authenticated AzureGraphAuth instance
            use_beta: If True, use the beta API endpoint
        """
        self.auth = auth
        self.logger = logging.getLogger(__name__)
        
        # Determine base URL
        if use_beta:
            self.base_url = "https://graph.microsoft.com/beta"
        else:
            self.base_url = "https://graph.microsoft.com/v1.0"
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for API requests.
        
        Returns:
            Dictionary of HTTP headers
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request to the Graph API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters
            
        Returns:
            Response JSON or None if request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params
            )
            
            response.raise_for_status()
            
            # Some responses (like DELETE) may not have content
            if response.status_code == 204:
                return {"status": "success"}
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            if e.response is not None:
                self.logger.error(f"Response: {e.response.text}")
            return None
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")
            return None
    
    # User Management Methods
    
    def list_users(self, top: int = 10, select: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        List users in the organization.
        
        Args:
            top: Number of users to return (default: 10)
            select: List of properties to return
            
        Returns:
            Response containing user list or None
        """
        params = {"$top": top}
        if select:
            params["$select"] = ",".join(select)
        
        return self._make_request("GET", "/users", params=params)
    
    def get_user(self, user_id: str, select: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by ID or UPN.
        
        Args:
            user_id: User ID or User Principal Name
            select: List of properties to return
            
        Returns:
            User information or None
        """
        params = {}
        if select:
            params["$select"] = ",".join(select)
        
        return self._make_request("GET", f"/users/{user_id}", params=params)
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new user.
        
        Args:
            user_data: User properties (accountEnabled, displayName, 
                      mailNickname, userPrincipalName, passwordProfile, etc.)
            
        Returns:
            Created user information or None
        """
        return self._make_request("POST", "/users", data=user_data)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing user.
        
        Args:
            user_id: User ID or User Principal Name
            user_data: Properties to update
            
        Returns:
            Response or None
        """
        return self._make_request("PATCH", f"/users/{user_id}", data=user_data)
    
    def delete_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Delete a user.
        
        Args:
            user_id: User ID or User Principal Name
            
        Returns:
            Response or None
        """
        return self._make_request("DELETE", f"/users/{user_id}")
    
    # Group Management Methods
    
    def list_groups(self, top: int = 10, select: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        List groups in the organization.
        
        Args:
            top: Number of groups to return (default: 10)
            select: List of properties to return
            
        Returns:
            Response containing group list or None
        """
        params = {"$top": top}
        if select:
            params["$select"] = ",".join(select)
        
        return self._make_request("GET", "/groups", params=params)
    
    def get_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific group by ID.
        
        Args:
            group_id: Group ID
            
        Returns:
            Group information or None
        """
        return self._make_request("GET", f"/groups/{group_id}")
    
    def create_group(self, group_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new group.
        
        Args:
            group_data: Group properties (displayName, mailEnabled, 
                       mailNickname, securityEnabled, etc.)
            
        Returns:
            Created group information or None
        """
        return self._make_request("POST", "/groups", data=group_data)
    
    def list_group_members(self, group_id: str) -> Optional[Dict[str, Any]]:
        """
        List members of a group.
        
        Args:
            group_id: Group ID
            
        Returns:
            Response containing group members or None
        """
        return self._make_request("GET", f"/groups/{group_id}/members")
    
    def add_group_member(self, group_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Add a member to a group.
        
        Args:
            group_id: Group ID
            user_id: User ID to add
            
        Returns:
            Response or None
        """
        data = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }
        return self._make_request("POST", f"/groups/{group_id}/members/$ref", data=data)
    
    # Application Management Methods
    
    def list_applications(self, top: int = 10) -> Optional[Dict[str, Any]]:
        """
        List applications in the organization.
        
        Args:
            top: Number of applications to return (default: 10)
            
        Returns:
            Response containing application list or None
        """
        params = {"$top": top}
        return self._make_request("GET", "/applications", params=params)
    
    def get_application(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific application by ID.
        
        Args:
            app_id: Application ID
            
        Returns:
            Application information or None
        """
        return self._make_request("GET", f"/applications/{app_id}")
    
    # Organization Information
    
    def get_organization(self) -> Optional[Dict[str, Any]]:
        """
        Get organization information.
        
        Returns:
            Organization information or None
        """
        return self._make_request("GET", "/organization")
    
    # Generic Methods
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Make a generic GET request to any Graph API endpoint.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response or None
        """
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make a generic POST request to any Graph API endpoint.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            
        Returns:
            Response or None
        """
        return self._make_request("POST", endpoint, data=data)
    
    def patch(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make a generic PATCH request to any Graph API endpoint.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            
        Returns:
            Response or None
        """
        return self._make_request("PATCH", endpoint, data=data)
    
    def delete(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Make a generic DELETE request to any Graph API endpoint.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Response or None
        """
        return self._make_request("DELETE", endpoint)
