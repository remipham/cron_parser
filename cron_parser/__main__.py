
import sys

from cron_parser.cron import Cron

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cron_parser '<cron_string>'")
        sys.exit(1)
    cron_string = sys.argv[1]
    try:
        cron = Cron(cron_string)
        cron.print_output()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
