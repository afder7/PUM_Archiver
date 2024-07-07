import os
import random
import string


def run_cmd(fname, key=None, encode=True):
    cmd = f"python3 main.py -{'e' if encode else 'd'} {fname}"
    if key:
        cmd += f" {key}"
    print(f"Running {cmd}")
    os.system(cmd)


def check(key=None):
    filenames = []

    for filename in os.listdir('samples/'):
        if os.path.splitext(filename)[1] == ".txt":
            filenames.append(filename)
        else:
            os.remove(os.path.join('samples/', filename))  # get rid of unused files (typically *.par ones)

    for fname in filenames:
        fname = os.path.join('samples/', fname)
        run_cmd(fname, key)
        rname = fname.replace('.txt', '.par')
        if not os.path.exists(rname):
            print(f"ERROR: There is no encoded file here: {rname}")
            exit(1)
        if os.path.getsize(fname) <= os.path.getsize(rname):
            print("ERROR: The original file size was less or equal than 'pared'")
            exit(1)
        with open(fname) as f:
            original = f.read()
        os.remove(fname)
        run_cmd(rname, key, False)
        if not os.path.exists(fname):
            print(f"ERROR: There is no decoded file here: {fname}")
            exit(1)
        with open(fname) as f:
            processed = f.read()
        if original != processed:
            print("ERROR: Original text is different from processed")
            exit(1)


print("Check encoding-decoding without crypto")
check()
with open('mark.txt') as f:
    mark = int(f.read())
    if mark == 5:
        print("Check crypto")
        check(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)))
