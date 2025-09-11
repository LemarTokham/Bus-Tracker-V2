# Bus Tracker V2
Building an improved bus tracker this time using react/ts and the google maps api

# Current Features
- Currently displays a select number of bus stops.
- Each stop can be clicked on, showing the buses from the selected stop and from the relevant company (arriva/ stagecoach)
- Each bus can be clicked on, once clicked, the location of each bus of that line is displayed on the map
- Polling of API happens every 10 seconds to get new location data automatically
- Shows relevant buses from both arriva and stagecoach

# Features in progress
- Letting the user know which of the bus options have no buses out on the roads
- Legend for icons
- Showing buses incoming to the bus stop
- Only showing buses within the Liverpool region


# Image of UI + console
- Yellow pins are the bus stops
- Red pins are the busses from selected bus (the "17" highlighted in blue)
![UI image](images/bus-location-image.png)

# Current blockers
