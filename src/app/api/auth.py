import msal
import jwt
from datetime import datetime


async def auth():
    # Data for auth
    accessToken = None
    tenantID = 'e8c92bf5-2138-43f0-8e58-0c0382d2334e'
    authority = 'https://login.microsoftonline.com/' + tenantID
    clientID = 'd5918b13-ed1a-44b9-b6c3-bd08c8d209d6'
    scope = ['https://graph.microsoft.com/.default']
    thumbprint = 'BF399E409ECD6EEA08D9E389ED31D5748B16894B'
    certfile = 'server.pem'

    def msal_certificate_auth(clientID, scope, authority, thumbprint, certfile):
        app = msal.ConfidentialClientApplication(clientID, authority=authority,
                                                 client_credential={"thumbprint": thumbprint,
                                                                    "private_key": open(certfile).read()})
        result = app.acquire_token_for_client(scopes=scope)
        return result

    def msal_jwt_expiry(accessToken):
        decodedAccessToken = jwt.decode(accessToken, verify=False)
        tokenExpiry = datetime.fromtimestamp(int(decodedAccessToken['exp']))
        print("Token Expires at: " + str(tokenExpiry))
        return tokenExpiry
        # Auth

    try:
        if not accessToken:
            try:
                # Get a new Access Token using Client Credentials Flow and a Self Signed Certificate
                accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)
            except Exception as err:
                print('Error acquiring authorization token. Check your tenantID, clientID and certficate thumbprint.')
                print(err)
        tokenExpiry = msal_jwt_expiry(accessToken['access_token'])
        time_to_expiry = tokenExpiry - datetime.now()
        if time_to_expiry.seconds < 600:
            print("Access Token Expiring Soon. Renewing Access Token.")
            accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)

    except Exception as err:
        print(err)
    # Query
    return accessToken