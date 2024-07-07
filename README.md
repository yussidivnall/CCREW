# Channel Crossing Research Utilities
These are a set of utilities designed to assist in developing an understanding of response to emergencies at sea.
Our goal is to make every journey non lethal.

These utilities monitors and alerts when potentially dangerous situations occur.
Tools for a safer passage.

## Utilities

### Maritime
#### generate_csv
A service which listens to AIS updates from AISStream and records ais positioning data of vessels (boats and SAR planes).
for each of those, it generates two csv files, a "state", and a "log", which it updates periodically.

#### plot csv

Injest the CSVs to plot a map using plotly library.
Expose Dash interface

#### post
Post to discord

### Weather

#### Daily Forecast post

## Usage
You probably want to be in a python virtual environment!

`pip install -r requirements.txt`
In one terminal run `python track.py`
This will generate and update log files files in "data/boats.log.csv" and "data/aircrafts.log.csv".
Let it run while using the application
In another start the Dash application, to monitor `python app.py` and browse to http://localhost:8050
