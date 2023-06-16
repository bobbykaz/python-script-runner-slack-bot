
import sys

def search_issues(ticket, lable):
    print(f"ticket: {ticket} - label: {lable}")

def main(args):
    print("pretending to search for tickets in your ticket system...")
    search_issues("ab-123", "done")
    search_issues(args[0], args[1])

if __name__ == "__main__":
    main(sys.argv)