def handler(event, context):
    """Simple token-based authorizer"""
    auth_token = event.get('headers', {}).get('Authorization')
    
    # Demo policy - you should implement proper token validation
    policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow' if auth_token else 'Deny',
                'Resource': event['methodArn']
            }]
        }
    }
    
    return policy 