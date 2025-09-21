# Bus Tracker V2
Building an improved bus tracker this time using react/ts and the google maps api

# Current Features
- Currently displays a select number of bus stops.
- Each stop can be clicked on, showing the buses from the selected stop and from the relevant company (arriva/ stagecoach)
- Each service can be clicked on, once clicked, the location of each bus of that service is displayed on the map
- User gets told if a selected service has no buses out on the roads
- Polling of API happens every 10 seconds to get new location data automatically

# Features in progress
- PANDAS MIGRATION COMPLETE!!!!!!: Switched to using pandas dataframes for processing the bus location data 
- Legend for icons
- Showing buses incoming to the bus stop
- Only showing buses within the Liverpool region as sometimes buses with the same service number in other cities are displayed
- Someway to show the uer the 10 second tracking timer for bus location update (maybe a spinner?)

# What i've learnt
- Using and manipulating dataframes
- understanding how to define types and interfaces
- The importance of decoupling code so if one parts fails you can go directly in that part and fix it rather than fix everything all over again or restart


# Image of UI + console
- Yellow pins are the bus stops
- Red pins are the busses from selected bus (the "10A" highlighted in blue)
![UI image](images/map-image.png)

# Current blockers
- Code cleaning (IT LOOKS HORRIBLE TRUST THE PROCESS i just needed it to work after the migration to pandas)

