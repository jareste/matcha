from models import insert_random_users
import sys

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    insert_random_users(count)

