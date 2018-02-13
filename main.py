from multiprocessing import Process, Queue
import json
import requests
import time

def live_loop(q):
    while True:
        game_data = get_game_data()
        q.put(game_data)
        time.sleep(5)

def get_game_data():
    url = "https://statsapi.web.nhl.com/api/v1/game/2017020861/feed/live"
    req = requests.get(url)
    return req.json()

def printer(q):
    while True:
        print(q.get())
        time.sleep(1)

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=live_loop, args=(q,))
    p2 = Process(target=printer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()