/** Renders wherever the API marks a record `synthetic: true`. Never hide this — see AGENTS.md rule 6. */
export default function SyntheticBadge() {
  return (
    <span className="inline-block rounded bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-800">
      Sample data — not a live record
    </span>
  )
}
