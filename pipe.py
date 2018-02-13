from multiprocessing import Process, Pipe
import time

def c(conn):
    for _ in list(range(5)):
        conn.send([42, None, 'hello'])
        time.sleep(2)
    conn.send(9999)  
    conn.close()

def p(conn):
    while True:
        data = parent_conn.recv()
        if data == 9999:
            break
        print(data)

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p1 = Process(target=c, args=(child_conn,))
    p2 = Process(target=p, args=(parent_conn,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
