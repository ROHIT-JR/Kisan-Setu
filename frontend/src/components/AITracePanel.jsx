import { useState } from 'react'

/** Makes the Google AI routing decision visible to a judge instead of merely claimed. See prompt.md §6. */
export default function AITracePanel({ trace }) {
  const [open, setOpen] = useState(false)
  if (!trace) return null

  return (
    <div className="mt-4 rounded border border-stone-200 text-sm">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full px-3 py-2 text-left font-medium text-stone-700"
      >
        {open ? '▾' : '▸'} How this answer was produced
      </button>
      {open && (
        <div className="space-y-1 border-t border-stone-200 px-3 py-2 text-stone-600">
          <div>CNN confidence: {trace.cnn_confidence ?? 'n/a'}</div>
          <div>Routed to Gemini: {String(trace.routed_to_gemini)}</div>
          <div>CNN latency: {trace.cnn_ms ?? 'n/a'} ms</div>
          <div>Gemini latency: {trace.gemini_ms ?? 'n/a'} ms</div>
          <div>Cache hit: {String(trace.cache_hit)}</div>
        </div>
      )}
    </div>
  )
}
