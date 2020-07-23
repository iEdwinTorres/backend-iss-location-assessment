#!/usr/bin/env python

__author__ = "Edwin Torres"

import requests
import time
import turtle

iss_icon = "iss.gif"
world_map = "map.gif"
base_url = "http://api.open-notify.org"


def get_astronaut_info():
    """Gets a list of the astronauts currently on the ISS."""
    req = requests.get(base_url + "/astros.json")
    req.raise_for_status()
    return req.json()["people"]


def locate_iss():
    """Gets the current coordinates of the ISS and timestamp."""
    req = requests.get(base_url + "/iss-now.json")
    req.raise_for_status()
    position = req.json()["iss_position"]
    longitude = float(position["longitude"])
    latitude = float(position["latitude"])
    return longitude, latitude


def map_iss(longitude, latitude):
    """Draws a world map and places the ISS icon at its current coordinates"""
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_icon)
    iss = turtle.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90)
    iss.penup
    iss.goto(longitude, latitude)
    return screen


def compute_rise_time(longitude, latitude):
    params = {"lon": longitude, "lat": latitude}
    req = requests.get(base_url + "/iss-pass.json", params=params)
    req.raise_for_status()
    passover_time = req.json()["response"][1]["risetime"]
    return time.ctime(passover_time)


def main():
    astro_dict = get_astronaut_info()
    for astro in astro_dict:
        print(" - {} in {}".format(astro["name"], astro["craft"]))

    longitude, latitude = locate_iss()
    print(
        "Current ISS coordinates: longitude={:.02f} latitude={:.02f}".format(
            longitude, latitude
        )
    )

    screen = None
    try:
        screen = map_iss(longitude, latitude)
        indy_lon = -86.158068
        indy_lat = 39.768403
        location = turtle.Turtle()
        location.penup()
        location.color("red")
        location.goto(indy_lon, indy_lat)
        location.dot(5)
        location.hideturtle()
        next_pass = compute_rise_time(indy_lon, indy_lat)
        location.write(next_pass, align="center", font=("Arial", 12, "normal"))
    except RuntimeError as error:
        print("ERROR: problem loading graphics: " + str(error))
    if screen is not None:
        screen.exitonclick()


if __name__ == "__main__":
    main()
