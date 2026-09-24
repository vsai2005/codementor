/**
 * Safe redirect validator and sanitizer for open-redirect attack prevention.
 *
 * Guarantees that redirected URLs are strictly same-origin relative paths.
 * Rejects:
 * - Protocol-relative URLs (e.g. "//evil.com")
 * - Windows UNC or backslash path tricks (e.g. "/\\evil.com", "\\evil.com")
 * - Explicit URI schemes (e.g. "https:", "http:", "javascript:", "data:", "vbscript:")
 * - Direct authentication loop paths (e.g. "/login", "/register", "/api/auth")
 * - Control characters, newlines, null bytes, or non-strings
 */
export function getSafeRedirect(
  target: string | null | undefined,
  fallback: string = "/dashboard",
): string {
  if (!target || typeof target !== "string") {
    return fallback;
  }

  const trimmed = target.trim();
  if (!trimmed) {
    return fallback;
  }

  // Must begin with a single slash
  if (!trimmed.startsWith("/")) {
    return fallback;
  }

  // Reject protocol-relative or Windows-style paths
  if (trimmed.startsWith("//") || trimmed.startsWith("/\\")) {
    return fallback;
  }

  // Reject backslashes anywhere in the path to prevent browser parsing normalization tricks
  if (trimmed.includes("\\")) {
    return fallback;
  }

  // Reject explicit schemes (e.g., "javascript:", "data:", "https:")
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(trimmed)) {
    return fallback;
  }

  try {
    // Parse against a dummy base origin to inspect resolved components
    const parsed = new URL(trimmed, "http://localhost");
    if (parsed.origin !== "http://localhost") {
      return fallback;
    }

    // Prevent direct auth loops
    const normalizedPath = parsed.pathname.toLowerCase();
    if (
      normalizedPath === "/login" ||
      normalizedPath === "/register" ||
      normalizedPath.startsWith("/api/auth")
    ) {
      return fallback;
    }

    return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  } catch {
    return fallback;
  }
}
