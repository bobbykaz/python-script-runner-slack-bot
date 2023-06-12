import sys
import time

def main(args):
    print(f"sample thing as if this were a real script: args: {args}")
    for i in range(0,10):
        print(f'step {i}')
        time.sleep(3)

if __name__ == "__main__":
    main(sys.argv)