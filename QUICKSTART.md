# Quick Start Guide

Get started with Azure Graph API in 5 minutes!

## Prerequisites

- Python 3.7+
- Azure AD application with client credentials
- Required permissions granted with admin consent

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
# Copy the template
cp config.template.json config.json

# Edit config.json with your credentials
# You need: tenant_id, client_id, client_secret
```

### 3. Test Your Setup

```bash
python example_basic.py
```

## Common Commands

### Using the Utility Script

```bash
# List users
python utils.py list-users

# List groups
python utils.py list-groups

# Get specific user
python utils.py get-user user@domain.com

# Get organization info
python utils.py org-info

# List group members
python utils.py list-group-members <group-id>
```

### Using in Python Code

```python
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient

# Authenticate
auth = AzureGraphAuth()
auth.authenticate_client_credentials()

# Create client and make requests
client = GraphAPIClient(auth)
users = client.list_users(top=10)
```

## Common Issues

**Authentication fails?**
- Verify credentials in config.json
- Check that admin consent was granted

**Permission denied?**
- Ensure Application permissions (not Delegated)
- Grant admin consent for the tenant

**Module not found?**
- Run: `pip install -r requirements.txt`

## What's Next?

1. **Read the full documentation**: Check [README.md](README.md)
2. **Detailed setup guide**: See [SETUP.md](SETUP.md)
3. **Explore examples**: Run `example_basic.py` and `example_advanced.py`
4. **Customize**: Modify the scripts for your specific needs

## Need Help?

- Review [SETUP.md](SETUP.md) for detailed configuration steps
- Check [Microsoft Graph API docs](https://docs.microsoft.com/en-us/graph/api/overview)
- Review Azure AD sign-in logs for authentication issues

## Security Reminder

- Never commit `config.json` to version control
- Store secrets securely (use Azure Key Vault in production)
- Rotate client secrets regularly
- Use least privilege permissions
