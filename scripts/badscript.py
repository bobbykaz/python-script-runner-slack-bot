
import sys

def search_issues_but_explode(ticket, lable):
    raise Exception(f'Sample Exception {ticket}/{lable}')

def main(args):
    print("sample thing as if this were a real script")
    search_issues_but_explode("ab-123", "done")

if __name__ == "__main__":
    main(sys.argv)