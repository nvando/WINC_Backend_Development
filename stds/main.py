# Leave these lines untouched
__winc_id__ = "8c2e6882503c4baa9ce2e050497c3f2f"
__human_name__ = "stds"


import sys


def main():
    # read text from stdin
    txt = sys.stdin.read()
    arg = sys.argv[1]
    char_count = txt.count(arg)

    # filters a given character from the text and count the number of replaced items
    filtered_txt = txt.replace(arg, "")

    # Print the result to stdout
    sys.stdout.write(filtered_txt)

    # Print the total number of removed characters to stderr
    sys.stderr.write(str(char_count))


if __name__ == "__main__":
    main()
