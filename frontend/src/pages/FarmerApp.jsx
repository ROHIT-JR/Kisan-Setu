import { useState } from 'react'
import SyntheticBadge from '../components/SyntheticBadge.jsx'
import AITracePanel from '../components/AITracePanel.jsx'
import en from '../i18n/en.json'

export default function FarmerApp() {
  const [image, setImage] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleDiagnose(e) {
    e.preventDefault()
    if (!image) return
    setLoading(true)
    const form = new FormData()
    form.append('image', image)
    form.append('district_code', '581')
    form.append('lang', 'en')
    try {
      const res = await fetch('/api/diagnose', { method: 'POST', body: form })
      setResult(await res.json())
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-xl p-6">
      <h1 className="mb-4 text-xl font-semibold">{en.app_title}</h1>
      <form onSubmit={handleDiagnose} className="space-y-3">
        <label className="block text-sm text-stone-600">{en.farmer_upload_prompt}</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files?.[0] ?? null)}
          className="block w-full text-sm"
        />
        <button
          type="submit"
          disabled={!image || loading}
          className="rounded bg-green-700 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading ? '...' : en.diagnose_button}
        </button>
      </form>

      {result && (
        <div className="mt-6 rounded border border-stone-200 p-4">
          <div className="mb-2 flex items-center gap-2">
            <h2 className="font-medium">{result.disease_display}</h2>
            {result.synthetic && <SyntheticBadge />}
          </div>
          <p className="text-sm text-stone-600">{result.caveat}</p>
          <ul className="mt-2 list-disc pl-5 text-sm">
            {result.treatment_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>
          <AITracePanel trace={result.trace} />
        </div>
      )}
    </div>
  )
}
