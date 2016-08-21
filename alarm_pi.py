import atexit
import queue

import web
import threads
import utils
import manager


background_thread = None
clock_thread = None
comm = queue.Queue()
        
        
def kill_background():
    global clock_thread

    if clock_thread is not None:
        clock_thread.signal.set()


atexit.register(kill_background)

if __name__ == '__main__':
    manager.load()
    
    #background_thread = threading.Thread(target=Background.runner, args=(comm,))
    #background_thread.start()
    #comm.put({'cmd': 'alarms', 'alarms': alarms})
    
    clock_thread = utils.RepeatingTimer(1, threads.clock)
    clock_thread.start()

    web.app.run(host='0.0.0.0')
