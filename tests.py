#!/usr/bin/python3

import transfer
import io
import time
import os

p1 = transfer.PipeServer(5001)
p2 = transfer.PipeServer(5002)

time.sleep(3)
c = p1.connect("127.0.0.1", 5002)
c.sendFile("test.txt", io.BytesIO(b"Der Inhalt einer Testdatei..."))
time.sleep(1)
if os.path.exists("test.txt"):
    print("Test efolgreich!!!")
c.close()
