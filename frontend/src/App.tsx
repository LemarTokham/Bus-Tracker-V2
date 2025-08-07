import './App.css'
import {
    APIProvider,
    Map,} from '@vis.gl/react-google-maps';
  
import type {MapCameraChangedEvent} from '@vis.gl/react-google-maps'
import { AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import { useState } from 'react';
import type { Marker } from '@googlemaps/markerclusterer';

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

  }
  
  const [busStops, setBusStops] = useState<BusStop[]>([])
  console.log("hit", busStops[0])
  return (
    <div>
    <APIProvider apiKey={api_key}>
      <Map
      onCameraChanged={(ev: MapCameraChangedEvent)=> console.log(ev.detail.zoom)}
       style={{width: 800, height: 800} }
      defaultCenter={{ lat: 53.400002, lng:-2.983333 }}
      defaultZoom={13}
      mapId={'bdf9633d0aa1b62af7a1a582'}
      >
    
      {busStops.map((busStop)=>(
        <AdvancedMarker
        key={busStop.name}
        position={busStop.location}
        >
          <Pin background={'#FBBC04'} glyphColor={'#000'} borderColor={'#000'} />
        </AdvancedMarker>
      ))}
      </Map>
    </APIProvider>
    <button onClick={async () => {
      const result = await getBusStopData()
      setBusStops(result)
      console.log(result)
    }}>Call bus stops</button>
    </div>
  )
}






export default App
