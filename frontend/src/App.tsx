import './App.css'
import {
    APIProvider,
    Map,} from '@vis.gl/react-google-maps';
import { AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import { useState } from 'react';

// API key
const api_key = import.meta.env.VITE_API_KEY

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
      return bus_stops
  
  }catch (error){
    console.log(error)
    return []
  }
}

function App() {
  interface BusStop {
    location: google.maps.LatLngLiteral
    name: string;
    buses: [number]
  }
  
  const [busStops, setBusStops] = useState<BusStop[]>([])
  const [stopClicked, setStopClicked] = useState<boolean>(false)
  const [buses, setBuses] = useState<number[]>([])




  const handleClick = ( async ()=>{
    console.log("hi")
    const result = await getBusStopData()
    setBusStops(result)
  })

  const handleStopClick = ((busList: number[])=>{
    console.log(busList)
    setBuses(busList)
    setStopClicked(true)
  })


  return (
    <div>
        <button onClick={async () => handleClick()}>
        Show bus stops</button>
    {stopClicked && <p>Buses that stop here: {buses.map((bus, index) => { return (
      <span className='bus-name' onMouseOver={()=> {
      }} onClick={() => console.log(bus)} key={index}>"{bus}" </span>)
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
      </Map>
    </APIProvider>

    </div>
  )
}


export default App
