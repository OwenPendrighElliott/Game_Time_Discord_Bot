import re
def get_updates(log_file):
    useful_lines = []
    pat = re.compile(".+\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.+")
    with open(log_file, 'r') as log:
        for line in log.read().splitlines():
            if '[Server thread/INFO]' in line and "Rcon" not in line and "<" not in line and "lost connection: Disconnected" not in line and not pat.match(line):
                useful_lines.append(line)

    print_lines = []
    with open("MC_SERVER_PREV.log", "r") as prev:
        prev_lines = prev.read()

        for nline in useful_lines:

            if nline not in prev_lines:
                print_lines.append(nline)

    with open("MC_SERVER_PREV.log", 'w') as prev:
        for line in useful_lines:
            prev.write(line + "\n")

    return "\n".join([line for line in print_lines])