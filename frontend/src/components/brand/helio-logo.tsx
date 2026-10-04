import Link from "next/link";


interface HelioLogoProps {
  href?: string;
  compact?: boolean;
  className?: string;
}


export function HelioLogo({
  href = "/",
  compact = false,
  className = "",
}: HelioLogoProps) {
  return (
    <Link
      href={href}
      className={`group inline-flex items-center gap-3 ${className}`}
      aria-label="HelioSL home"
    >
      <span className="relative grid h-11 w-11 shrink-0 place-items-center overflow-hidden rounded-2xl border border-emerald-200/30 bg-gradient-to-br from-yellow-300 via-emerald-300 to-emerald-600 shadow-[0_10px_35px_rgba(52,211,153,0.28)]">
        <svg
          viewBox="0 0 48 48"
          aria-hidden="true"
          className="h-9 w-9 transition-transform duration-300 group-hover:scale-105"
        >
          <circle cx="34" cy="14" r="6" fill="#fff7bd" />
          <path
            d="M9 31.5 24 18l15 13.5V39H9z"
            fill="#064e3b"
            opacity=".92"
          />
          <path
            d="m13 31 11-9.5L35 31H13Z"
            fill="#d1fae5"
          />
          <path
            d="M16 29.4h16M18.7 26.9l-1.6 5.4M24 22.4v10M29.3 26.9l1.6 5.4"
            stroke="#059669"
            strokeWidth="1.2"
            strokeLinecap="round"
          />
          <path
            d="M21 39v-5h6v5"
            fill="#fef3c7"
          />
        </svg>
      </span>

      {!compact && (
        <span>
          <span className="block text-lg font-semibold tracking-tight text-white">
            HelioSL
          </span>
          <span className="block text-[9px] font-medium uppercase tracking-[0.24em] text-emerald-300/80">
            Energy intelligence
          </span>
        </span>
      )}
    </Link>
  );
}
