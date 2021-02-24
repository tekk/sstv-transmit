# SSTV-Transmit

This web app is used to run on a Raspberry Pi and transmit uploaded images (via web interface) using SSTV.
It's built using Python and Flask, SSTV sound generating is done by PySSTV library.
You can connect your cheap Baofeng using DIY cable to sound card.

### To install requirements, run:

```
pip3 install -r requirements.txt
```

and

```
sudo apt install python3-gst-1.0
```

### Then you can run the development server on port 5000 by running

```
python3 sstv-transmit.py
```

If you want to leave this app running in the background, you can use a `tmux` detached session, or add it to `init.d`

All credits goes to the creator of PySSTV. Huge thanks for an amazing lib.