# Channel Crossing Research Early Warning

These are a set of utilities designed to assist in developing an understanding of response to emergencies at sea.
Our goal is to make every journey non lethal, reduce where possible the risk to life and monitor the behviour of the emergency services to mitigate and prevent harm.

These utilities monitors and alerts when potentially dangerous situations occurs at sea.

Tools for a safer passage.

## Requirements


- AISStream [api_key](https://aisstream.io/documentation)
- Discord [webhook_url](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
Two points on a map to define the arena
A list of boats you would like to track

## Configurations
copy the example config to config.py `cp config.py.example config.py`.
edit the `config.py` file with your favourite text editor and set the following required configurations

- api_key - the AISStream api_key
- discord_webhook_url - the discord URL
- arena - the region of interest,   single bounding box defined as 
    `arena = [[[51.385, 0.909], [50.678, 2.667]]]`
- tracked boats in this format
````python
tracked_boats = [
    {
        "mmsi": 1234,
        "name": "EXACT BOAT NAME   ",
        "label": "Some label",
        "color": "red",
        "alerts": [
            {
                "name": "Boat Moving",
                "enable": "speed>=5",
                "disable": "speed<5",
            },
        ]
    },
    ...
]
```
the "alerts" are optional, and define the condition under which monitoring should be enabled and disabled. currently only able to raise an alert based on a boat's speed


## Using Docker
Run using `$docker compose up`
port 8050 should be opened for requests and accessible using postman, a browser, curl, etc
## Endpoints

- `/health` - health endpoing for heartbeat
- `/snapshot` - generate and post a snapshot image to discord

    for example `curl localhost:8050/health`

## Setup

Create a python virtual environment

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy over `config.py.example` to `config.py`

```sh
cp config.py.example config.py
```



In order to monitor maritime traffic, you need to get an [API key](https://aisstream.io/) for the AISTream service.
One you have it, edit the file `config.py` using your text editor of choice which is vi to change the line `api_key = "Your AISStream API key"`

If you wish to use the `post.py` utility, to post a message to a discord channel, you will also need to get an API key to [discord developer portal](https://discord.com/developers/applications/), and create a bot with the permissions to send a message and attach files. see [here](https://realpython.com/how-to-make-a-discord-bot-python/) for a guide on how to do this.

once this is done, also update the `DISCORD API TOKEN` and `DISCORD CHANNEL ID`, which you can find using discord [as described here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID#h_01HRSTXPS5FMK2A5SMVSX4JW4E)

The Arena defines two points on a map, this is the area we will monitor, you can use a service such as [this](https://www.latlong.net/) to define the region of interest

## Utilities

running `python track.py` will begin the monitoring service. it will create two csv files in the `data/` directory, each showing a log of position reports for boats and for Search and Rescue aircraft.

Once this is running, you can use `python app.py` to start a dash server, you should then be able to browse to http://localhost:8050 and see an updating map of the vessels in the region we defined above.

You can also use `python snap.py` to generate a snapshot image, which will be saves in `images/snapshot.png`
You can then post this to discord (provided you configured your bot), using `python post.py`.
