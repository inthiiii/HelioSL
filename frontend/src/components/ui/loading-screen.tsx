interface LoadingScreenProps {
  label?: string;
}


export function LoadingScreen({
  label = "Preparing your HelioSL experience",
}: LoadingScreenProps) {
  return (
    <main
      className="grid min-h-screen place-items-center bg-neutral-950 px-6 text-white"
      role="status"
      aria-live="polite"
    >
      <div className="w-full max-w-sm text-center">
        <div className="mx-auto grid h-16 w-16 place-items-center rounded-3xl border border-emerald-400/20 bg-emerald-400/10 shadow-[0_0_60px_rgba(52,211,153,0.14)]">
          <span className="h-7 w-7 animate-spin rounded-full border-2 border-emerald-300/25 border-t-emerald-300" />
        </div>
        <p className="mt-6 text-sm font-medium text-white">
          {label}
        </p>
        <p className="mt-2 text-xs text-neutral-500">
          Bringing your energy insights together
        </p>
        <div className="mt-6 h-1.5 overflow-hidden rounded-full bg-neutral-800">
          <div className="heliosl-loading-bar h-full w-2/5 rounded-full bg-gradient-to-r from-emerald-500 to-yellow-300" />
        </div>
      </div>
    </main>
  );
}
