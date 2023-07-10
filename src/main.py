from pathlib import Path
import logging
import sys
main_parent_path = Path(__file__).parent
sys.path.insert(1, str(main_parent_path.parent))
from expense_tracker import confirm_proceeding_with_parameters, verify_user_inputs


def main(argv: list):
    try:
        month, year = verify_user_inputs(argv)
        confirm_proceeding_with_parameters(month, year)
    except ValueError as ve:
        logging.error(f"{ve}\n")
        sys.exit(1)
    except KeyboardInterrupt as ki:
        logging.info(f"{ki}\n")
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s | %(levelname)s\t| %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    try:
        main(sys.argv)
    except SystemExit as exit_code:
        sys.exit(exit_code)
    except BaseException as e:
        logging.error(f"{e}\n")
        sys.exit(2)
