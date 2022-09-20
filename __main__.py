import sys
from .manage import main


if __name__ == "__main__":
    sys.argv = ["manage.py", "runserver"]
    main()
