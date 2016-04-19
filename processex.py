import subprocess

def main():

    cmd = 'python -u test.py'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, bufsize=1)

    while p.poll() is None:
        l = p.stdout.readline()
        print l

    print p.stdout.read()
        

if __name__ == '__main__':

    main()
