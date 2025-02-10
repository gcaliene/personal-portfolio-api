from src.config import get_db_path, get_db_url

def main():
    print(f"Database Path: {get_db_path()}")
    print(f"Database URL: {get_db_url()}")

if __name__ == "__main__":
    main() 