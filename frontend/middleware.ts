import { NextResponse, type NextRequest } from "next/server";

/**
 * Client-IP attestation for the /api proxy (Vercel -> Render).
 *
 * The backend rate-limits per client IP, but behind this proxy it only sees the platform's
 * address. On Vercel, the platform overwrites x-forwarded-for / x-real-ip with the real
 * client address (clients cannot set them), so this middleware copies that value into
 * x-codementor-client-ip and proves it came from here with x-codementor-proxy-auth =
 * PROXY_SHARED_SECRET (server-only env var, same value as on the backend).
 *
 * Attestation happens only on Vercel with the secret configured. Anywhere else (local
 * `next dev` / `next start`) incoming forwarding headers are client-controlled, so nothing
 * is attested and the backend falls back to the socket peer. Client-supplied copies of the
 * attestation headers are always removed.
 */
const CLIENT_IP_HEADER = "x-codementor-client-ip";
const PROXY_AUTH_HEADER = "x-codementor-proxy-auth";

function platformClientIp(request: NextRequest): string | null {
  const raw =
    request.headers.get("x-vercel-forwarded-for") ??
    request.headers.get("x-real-ip") ??
    request.headers.get("x-forwarded-for");
  const first = raw?.split(",")[0]?.trim();
  return first ? first : null;
}

export function middleware(request: NextRequest) {
  const headers = new Headers(request.headers);
  headers.delete(CLIENT_IP_HEADER);
  headers.delete(PROXY_AUTH_HEADER);

  const secret = process.env.PROXY_SHARED_SECRET;
  const onVercel = process.env.VERCEL === "1";
  const clientIp = onVercel && secret ? platformClientIp(request) : null;
  if (secret && clientIp) {
    headers.set(CLIENT_IP_HEADER, clientIp);
    headers.set(PROXY_AUTH_HEADER, secret);
  }

  return NextResponse.next({ request: { headers } });
}

export const config = {
  matcher: ["/api/:path*"],
};
