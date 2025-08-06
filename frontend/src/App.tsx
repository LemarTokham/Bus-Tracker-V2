import './App.css'
import {
    APIProvider,
    Map,} from '@vis.gl/react-google-maps';
  
import type {MapCameraChangedEvent} from '@vis.gl/react-google-maps'

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
  getBusStopData()
  return (
    <APIProvider apiKey={api_key}>
      <Map
      onCameraChanged={(ev: MapCameraChangedEvent)=> console.log(ev.detail.zoom)}
       style={{width: 800, height: 800} }
      defaultCenter={{ lat: 53.400002, lng:-2.983333 }}
      defaultZoom={13}
      mapId={'bdf9633d0aa1b62af7a1a582'}
      >
      </Map>
    </APIProvider>
  )
}

export default App
