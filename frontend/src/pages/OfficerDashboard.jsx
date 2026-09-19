import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import en from '../i18n/en.json'

export default function OfficerDashboard() {
  const [districts, setDistricts] = useState([])

  useEffect(() => {
    fetch('/api/districts')
      .then((r) => r.json())
      .then(setDistricts)
      .catch(() => setDistricts([]))
  }, [])

  function exportCsv() {
    const header = 'lgd_code,name,state,lat,lon,agro_climatic_zone\n'
    const rows = districts
      .map((d) => [d.lgd_code, d.name, d.state, d.lat, d.lon, `"${d.agro_climatic_zone}"`].join(','))
      .join('\n')
    const blob = new Blob([header + rows], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'districts.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  const center = districts.length ? [districts[0].lat, districts[0].lon] : [22.5, 78.9]

  return (
    <div className="mx-auto max-w-4xl p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold">{en.officer_dashboard_title}</h1>
        <button
          onClick={exportCsv}
          className="rounded border border-stone-300 px-3 py-1.5 text-sm"
        >
          Export CSV
        </button>
      </div>

      <div className="mb-4 grid grid-cols-3 gap-3 text-sm">
        <div className="rounded border border-stone-200 p-3">
          <div className="text-stone-500">Districts</div>
          <div className="text-lg font-semibold">{districts.length}</div>
        </div>
        <div className="rounded border border-stone-200 p-3">
          <div className="text-stone-500">Advisories issued</div>
          <div className="text-lg font-semibold">—</div>
        </div>
        <div className="rounded border border-stone-200 p-3">
          <div className="text-stone-500">Top disease this month</div>
          <div className="text-lg font-semibold">—</div>
        </div>
      </div>

      <MapContainer center={center} zoom={5} style={{ height: 400, width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
        {districts.map((d) => (
          <Marker key={d.lgd_code} position={[d.lat, d.lon]}>
            <Popup>
              {d.name}, {d.state}
              <br />
              {d.agro_climatic_zone}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}
