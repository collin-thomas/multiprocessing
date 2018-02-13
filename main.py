from multiprocessing import Process, Queue
import json
import requests
import time

def get_seconds_from_string(time_str):
    minute, second = time_str.split(':')
    return int(minute) * 60 + int(second)

def live_loop(q):
    game_time = None
    while True:
        game_data = get_game_data()
        new_game_time = game_data['liveData']['linescore']['currentPeriodTimeRemaining']
        new_game_time_seconds = get_seconds_from_string(new_game_time)
        if game_time:
            game_time_seconds = get_seconds_from_string(game_time)
        else:
            game_time_seconds = 0
        if game_time_seconds != new_game_time_seconds:
            game_time = new_game_time
            q.put(game_time)
        time.sleep(3)

def get_game_data():
    url = "https://statsapi.web.nhl.com/api/v1/game/2017020862/feed/live"
    req = requests.get(url)
    return req.json()

def blocking_printer(q):
    while True:
        print('waiting')
        game_data = q.get()
        print(game_data)
        time.sleep(1)

def nonblocking_printer(q):
    while True:
        print('waiting')
        try:
            game_data = q.get(False)
            print(game_data)
            # If `False`, the program is not blocked. `Queue.Empty` is thrown if 
            # the queue is empty
        except:
            pass
        time.sleep(1)

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=live_loop, args=(q,))
    #p2 = Process(target=blocking_printer, args=(q,))
    p2 = Process(target=nonblocking_printer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
