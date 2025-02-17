import re

def format_url_slug(title: str) -> str:
    """Convert a title to a URL-friendly slug.
    
    Example: "Hello World! (Test)" -> "hello-world-test"
    """
    # Convert to lowercase
    slug = title.lower()
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug 