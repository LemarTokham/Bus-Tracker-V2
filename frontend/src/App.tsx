import './App.css'
import {
    APIProvider,
    Map,} from '@vis.gl/react-google-maps';
import { AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import {useState, useRef } from 'react';


// API key
const api_key = import.meta.env.VITE_API_KEY


interface BusStop {
  location: google.maps.LatLngLiteral
  name: string;
  buses: BusObject
}

interface BusLocation {
  lat: number,
  lng: number
}

interface BusObject {
  arriva: string[]
  stagecoach: string[]
}


// Fetch bus stop information
async function getBusStopData(){
  const url = 'http://127.0.0.1:5000/api/bus-stops'
  try {
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const result = await response.json()
      const {bus_stops} = result
      // console.log(bus_stops)
      // console.log(result.bus_stops[2].buses.arriva)
      return bus_stops
  
  }catch (error){
    console.log(error)
    return []
  }
}


function App() {
  const [busStops, setBusStops] = useState<BusStop[]>([])
  const [stopClicked, setStopClicked] = useState<boolean>(false)
  const [arrivaBuses, setArrivaBuses] = useState<string[]>([])
  const [stageCoachBuses, setStageCoachBuses] = useState<string[]>([])
  const [busLocation, setBusLocation] = useState<BusLocation[]>([])
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined)

  const handleShowBusStopsClick = ( async ()=>{
    const result = await getBusStopData()
    setBusStops(result)
    console.log(result)
    console.log("hit", busStops)
  })


  const handleStopClick = ((busObject: BusObject)=>{
    console.log(busObject) // TODO rename as its now an object not a list

    const {arriva} = busObject
    const {stagecoach} = busObject

    console.log(arriva)
    console.log(stagecoach)

    setArrivaBuses(arriva)
    setStageCoachBuses(stagecoach)
    setStopClicked(true)
  })


  const handleBusClick = ( async (bus:string)=> {
    console.log(bus)
    clearTimeout(timeoutRef.current) // Clear previous polling operation which used previously selected bus
    
    const url = 'http://127.0.0.1:5000/api/buses'
    try{
      const response = await fetch(url, {
      method:'POST',
      body: JSON.stringify(bus),
      headers: {
        "Content-Type":"application/json"
      }
    })
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }


      const data = await response.json()
      console.log(data)
      setBusLocation(data.buses)

      timeoutRef.current = setTimeout(() => handleBusClick(bus), 10000) // Bus location updates every 10 seconds
    } catch (error) {
      console.log(error)
    }
  })

  const stopTracking = (() => {
    console.log("Stopped bus tracking")
    clearTimeout(timeoutRef.current)
  })


  return (
    <div>
      <button onClick={handleShowBusStopsClick}>
        Show bus stops
      </button>
      <button onClick={stopTracking}>
        Stop Tracking
      </button>

    {stopClicked && <p>Arriva: {arrivaBuses.map((bus, index) => { return (
      <span className='bus-name' 
      style={{cursor:'pointer'}}
      onClick={() => handleBusClick(bus)} 
      key={index}>"{bus}" 
      </span>)
    })} </p>}
    {stopClicked && <p>Stagecoach: {stageCoachBuses.map((bus, index) => { return (
      <span className='bus-name' 
      style={{cursor:'pointer'}}
      onClick={() => handleBusClick(bus)} 
      key={index}>"{bus}"
      </span>)
    })} </p>}
    
    <APIProvider apiKey={api_key}>
      <Map
       style={{width: 800, height: 800} }
      defaultCenter={{ lat: 53.400002, lng:-2.983333 }}
      defaultZoom={13}
      mapId={'bdf9633d0aa1b62af7a1a582'}
      disableDefaultUI={true}
      >
      {busStops.map((stop)=>(
        <AdvancedMarker
        onClick={() => handleStopClick(stop.buses)}
        key={stop.name}
        position={stop.location}
        >
          <Pin background={'#FBBC04'} glyphColor={'#000'} borderColor={'#000'} />
        </AdvancedMarker>
      ))}

      {busLocation.length > 0 && (
        busLocation.map((bus,index) => (
          <AdvancedMarker
          key={index}
          position={bus}
          >
            <Pin background={'#FF0000'} glyphColor={'#000'} borderColor={'#000'} />
          </AdvancedMarker>
        ))
      )}
      </Map>
    </APIProvider>
    </div>
  )
}

export default App