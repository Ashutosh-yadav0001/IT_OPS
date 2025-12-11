# Azure Graph API Setup Guide

This guide will walk you through setting up your Azure environment and configuring this application.

## Step 1: Create Azure AD Application

### Using Azure Portal

1. **Navigate to Azure Active Directory**
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Azure Active Directory"
   - Click on Azure Active Directory service

2. **Register a New Application**
   - In the left menu, click **App registrations**
   - Click **+ New registration**
   - Fill in the details:
     - **Name**: Choose a descriptive name (e.g., "IT-OPS-GraphAPI")
     - **Supported account types**: Select "Accounts in this organizational directory only"
     - **Redirect URI**: Leave blank (not needed for client credentials flow)
   - Click **Register**

3. **Note Your Application Details**
   - After registration, you'll see the application overview
   - **Copy and save**:
     - Application (client) ID
     - Directory (tenant) ID

4. **Create a Client Secret**
   - In the left menu, click **Certificates & secrets**
   - Click **+ New client secret**
   - Add a description (e.g., "IT-OPS-Secret")
   - Choose an expiration period (6 months, 12 months, or 24 months)
   - Click **Add**
   - **IMPORTANT**: Copy the secret **Value** immediately - you won't be able to see it again!

5. **Configure API Permissions**
   - In the left menu, click **API permissions**
   - Click **+ Add a permission**
   - Select **Microsoft Graph**
   - Select **Application permissions** (not Delegated)
   - Add the following permissions based on your needs:

   **Essential Permissions:**
   - `User.Read.All` - Read all users' full profiles
   - `Group.Read.All` - Read all groups

   **Optional Permissions** (add as needed):
   - `User.ReadWrite.All` - Read and write all users
   - `Group.ReadWrite.All` - Read and write all groups
   - `Application.Read.All` - Read applications
   - `Organization.Read.All` - Read organization info
   - `Directory.Read.All` - Read directory data

6. **Grant Admin Consent**
   - After adding permissions, click **Grant admin consent for [Your Organization]**
   - Click **Yes** to confirm
   - Verify all permissions show "Granted" status

### Using Azure CLI (Alternative)

```bash
# Login to Azure
az login

# Create the application
az ad app create \
  --display-name "IT-OPS-GraphAPI" \
  --sign-in-audience "AzureADMyOrg"

# Note the appId from the output

# Create a service principal
az ad sp create --id <appId>

# Create a client secret (note the password in output)
az ad app credential reset --id <appId>

# Add API permissions
az ad app permission add \
  --id <appId> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Role

# Grant admin consent
az ad app permission admin-consent --id <appId>
```

## Step 2: Configure the Application

1. **Copy Configuration Template**
   ```bash
   cp config.template.json config.json
   ```

2. **Edit config.json**
   
   Replace the placeholder values with your actual credentials:

   ```json
   {
     "azure": {
       "tenant_id": "your-actual-tenant-id",
       "client_id": "your-actual-client-id",
       "client_secret": "your-actual-client-secret",
       "authority": "https://login.microsoftonline.com/your-actual-tenant-id",
       "scope": ["https://graph.microsoft.com/.default"]
     },
     "graph_api": {
       "base_url": "https://graph.microsoft.com/v1.0",
       "beta_url": "https://graph.microsoft.com/beta"
     },
     "logging": {
       "level": "INFO",
       "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
     }
   }
   ```

   **Where to find each value:**
   - `tenant_id`: From App registrations > Overview > Directory (tenant) ID
   - `client_id`: From App registrations > Overview > Application (client) ID
   - `client_secret`: The value you copied when creating the client secret
   - `authority`: Replace the tenant_id in the URL with your actual tenant ID

3. **Verify Configuration**
   
   Your `config.json` should look like this (with real values):
   ```json
   {
     "azure": {
       "tenant_id": "12345678-1234-1234-1234-123456789abc",
       "client_id": "87654321-4321-4321-4321-abcdef123456",
       "client_secret": "abc123~DEF456_ghi789.jkl012",
       "authority": "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789abc",
       "scope": ["https://graph.microsoft.com/.default"]
     }
   }
   ```

## Step 3: Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt

# Optional: Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 4: Test Your Setup

Run the basic example to verify everything is working:

```bash
python example_basic.py
```

Expected output:
```
2024-XX-XX XX:XX:XX - __main__ - INFO - Authenticating with Azure AD...
2024-XX-XX XX:XX:XX - azure_auth - INFO - Successfully authenticated with Azure AD
2024-XX-XX XX:XX:XX - __main__ - INFO - Authentication successful!
2024-XX-XX XX:XX:XX - __main__ - INFO - 
--- Listing Users ---
2024-XX-XX XX:XX:XX - __main__ - INFO - User: John Doe (john.doe@domain.com)
...
```

## Common Issues and Solutions

### Issue: "Authentication failed"

**Solution:**
- Verify tenant_id, client_id, and client_secret are correct
- Check that the client secret hasn't expired
- Ensure there are no extra spaces in config.json

### Issue: "Insufficient privileges"

**Solution:**
- Verify API permissions are added as **Application** permissions (not Delegated)
- Ensure admin consent has been granted
- Wait a few minutes after granting consent for changes to propagate

### Issue: "AADSTS7000215: Invalid client secret"

**Solution:**
- The client secret has expired or is incorrect
- Create a new client secret in Azure Portal
- Update config.json with the new secret

### Issue: "Configuration file not found"

**Solution:**
- Ensure config.json exists in the same directory as the scripts
- Verify you copied from config.template.json
- Check file permissions

## Security Checklist

- [ ] config.json is listed in .gitignore
- [ ] Client secrets are stored securely
- [ ] API permissions follow least privilege principle
- [ ] Admin consent has been granted
- [ ] Client secret expiration is documented
- [ ] Access is monitored through Azure AD sign-in logs

## Next Steps

1. **Test basic operations**: Run `example_basic.py`
2. **Explore advanced features**: Run `example_advanced.py`
3. **Review permissions**: Ensure you have only the permissions you need
4. **Set up monitoring**: Configure Azure AD to monitor application sign-ins
5. **Plan secret rotation**: Set a reminder to rotate client secrets before expiration

## Additional Resources

- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) - Test API calls
- [Azure AD App Registration Docs](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Graph API Permissions Reference](https://docs.microsoft.com/en-us/graph/permissions-reference)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review Azure AD sign-in logs for error details
3. Consult Microsoft Graph API documentation
4. Open an issue in this repository
