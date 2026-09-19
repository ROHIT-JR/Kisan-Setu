import { useState } from 'react'
import en from '../i18n/en.json'

const empty = { lgd_code: '', name: '', state: '', lat: '', lon: '', agro_climatic_zone: '' }

export default function AddDistrict() {
  const [form, setForm] = useState(empty)
  const [status, setStatus] = useState(null)

  function set(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setStatus('saving')
    const res = await fetch('/api/districts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, lat: parseFloat(form.lat), lon: parseFloat(form.lon) }),
    })
    setStatus(res.ok ? 'done' : 'error')
    if (res.ok) setForm(empty)
  }

  return (
    <div className="mx-auto max-w-md p-6">
      <h1 className="mb-4 text-xl font-semibold">{en.add_district_title}</h1>
      <p className="mb-4 text-sm text-stone-600">
        Onboarding a district is a data entry, not a code change — this form proves it live.
      </p>
      <form onSubmit={submit} className="space-y-3">
        <input placeholder="LGD code" value={form.lgd_code} onChange={set('lgd_code')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" required />
        <input placeholder="District name" value={form.name} onChange={set('name')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" required />
        <input placeholder="State" value={form.state} onChange={set('state')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" required />
        <div className="flex gap-2">
          <input placeholder="Latitude" value={form.lat} onChange={set('lat')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" required />
          <input placeholder="Longitude" value={form.lon} onChange={set('lon')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" required />
        </div>
        <input placeholder="Agro-climatic zone" value={form.agro_climatic_zone} onChange={set('agro_climatic_zone')} className="w-full rounded border border-stone-300 px-3 py-1.5 text-sm" />
        <button type="submit" className="rounded bg-green-700 px-4 py-2 text-sm font-medium text-white">
          Add district
        </button>
      </form>
      {status === 'done' && <p className="mt-3 text-sm text-green-700">District added.</p>}
      {status === 'error' && <p className="mt-3 text-sm text-red-700">Failed to add district.</p>}
    </div>
  )
}
