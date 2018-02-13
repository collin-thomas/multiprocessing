from multiprocessing import Process, Pipe
import time

def f(conn):
    for _ in list(range(5)):
        conn.send([42, None, 'hello'])
        time.sleep(1)
    conn.send(9999)  
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    while True:
        data = parent_conn.recv()
        if data == 9999:
            break
        print(data)   # prints "[42, None, 'hello']"
    p.join()
