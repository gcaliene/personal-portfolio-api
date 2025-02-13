import boto3
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user(email: str, password: str, user_pool_id: str):
    client = boto3.client('cognito-idp')
    try:
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'}
            ],
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        )
        
        # Set permanent password
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=email,
            Password=password,
            Permanent=True
        )
        
        logger.info(f"Created user: {email}")
        return response
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

def get_token(username: str, password: str, client_id: str):
    client = boto3.client('cognito-idp')
    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        token = response['AuthenticationResult']['IdToken']
        logger.info(f"Got token for user: {username}")
        return token
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['create_user', 'get_token'], required=True)
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--user-pool-id', required=True)
    parser.add_argument('--client-id', required=True)
    
    args = parser.parse_args()
    
    if args.action == 'create_user':
        create_user(args.email, args.password, args.user_pool_id)
    elif args.action == 'get_token':
        token = get_token(args.email, args.password, args.client_id)
        print(f"Token: {token}") 