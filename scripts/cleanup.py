import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_stack(stack_name: str = 'article-api', region: str = 'us-east-2'):
    """Clean up a CloudFormation stack that's in ROLLBACK_COMPLETE state"""
    cf = boto3.client('cloudformation', region_name=region)
    
    try:
        logger.info(f"Deleting stack {stack_name}")
        cf.delete_stack(StackName=stack_name)
        waiter = cf.get_waiter('stack_delete_complete')
        logger.info("Waiting for stack deletion to complete...")
        waiter.wait(StackName=stack_name)
        logger.info("Stack deleted successfully")
    except cf.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            logger.info(f"Stack {stack_name} does not exist")
        else:
            logger.error(f"Error deleting stack: {e}")
            raise

if __name__ == "__main__":
    cleanup_stack() 