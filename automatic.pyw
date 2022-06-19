from threading import Thread
import background

shutdown = Thread(target=background.shutdown)
shutdown.start()