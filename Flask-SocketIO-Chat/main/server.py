#!/bin/env python
from app import create_app, socketio
import time
time.sleep(30)

app = create_app(debug=True)

socketio.run(app,host="0.0.0.0")
