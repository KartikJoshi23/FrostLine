const roles = [
  { label: "Freeze", className: "bg-freeze" },
  { label: "USDT moving", className: "bg-flow" },
  { label: "Our warnings", className: "bg-warning" },
  { label: "Public votes", className: "bg-vote" },
  { label: "TRON blocks", className: "bg-block" },
];

export function App() {
  return (
    <main className="grid min-h-dvh place-items-center bg-night-900 p-8">
      <div className="text-center">
        <h1 className="font-display text-6xl tracking-tight">FrostLine</h1>
        <p className="mt-3 text-mist">Early warning before a USDT freeze on TRON</p>
        <ul className="mt-10 flex flex-wrap justify-center gap-3">
          {roles.map((role) => (
            <li
              key={role.label}
              className="flex items-center gap-2 rounded-full bg-night-700 px-4 py-2 text-sm"
            >
              <span className={`size-2.5 rounded-full ${role.className}`} aria-hidden="true" />
              {role.label}
            </li>
          ))}
        </ul>
        <p className="mt-10 font-mono text-xs text-steel">
          Dashboard skeleton (P0). The scenes are built in P11 (plan 7.3).
        </p>
      </div>
    </main>
  );
}
