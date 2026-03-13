# Security Best Practices Report

## Executive Summary

- No critical or high-severity vulnerabilities were found in the current Next.js static docs site codebase.
- Deployment hardening is now present for both Vercel and generic static hosts through [vercel.json](vercel.json) and [public/_headers](public/_headers).
- Dependency review is clean for production packages: `npm audit --omit=dev` reported `0` vulnerabilities.
- One medium residual risk remains: the deployed CSP is a compatibility CSP and still allows inline scripts because Next.js static export emits inline runtime scripts.

## Findings

### Medium

#### SBP-001: CSP is compatibility-grade and still allows inline scripts

- Severity: Medium
- Location:
  - `vercel.json:25-53`
  - `public/_headers:13-20`
- Evidence:
  - `script-src 'self' 'unsafe-inline'`
- Impact:
  - This CSP still blocks third-party script origins by default, but it will not stop inline-script XSS if an attacker ever finds a DOM injection path.
- Why it remains:
  - Next.js static export currently emits inline runtime/bootstrap scripts, so a strict nonce/hash-only CSP is not practical in this build without deeper rendering changes or edge-side nonce injection.
- Recommended next step:
  - If you need a strict CSP posture, move to a deployment/runtime model that can attach nonces or hashes to the generated inline scripts and remove `'unsafe-inline'` from `script-src`.
- Mitigation already in place:
  - The repo audit found no `dangerouslySetInnerHTML`, `innerHTML`, `insertAdjacentHTML`, `eval`, `new Function`, `document.write`, `postMessage`, or client-exposed secret patterns in the app code.

### Low

#### SBP-002: Security header enforcement depends on the deployment platform honoring static-host config

- Severity: Low
- Location:
  - `vercel.json:1-58`
  - `public/_headers:1-20`
- Evidence:
  - Header policy is declared in hosting configuration files rather than enforced by runtime middleware.
- Impact:
  - If the final host ignores both `vercel.json` and `_headers`, cache policy and browser security headers will silently disappear.
- Recommended next step:
  - Verify deployed headers in CI or immediately after deploy with `curl -I <url>` or the browser network panel.

## Hardening Applied

- Added deployment security headers and cache-control policy:
  - `vercel.json:1-58`
  - `public/_headers:1-20`
- Disabled the `x-powered-by` header and enabled static-host-friendly output:
  - `next.config.ts:3-15`
- Reduced unnecessary route prefetching and trimmed navigation payload:
  - `lib/docs.ts:465-573`
  - `components/sidebar.tsx:23-67`
  - `components/home-page.tsx:11-103`
- Hardened outbound links with `noopener noreferrer`:
  - `components/site-header.tsx:37-45`
  - `components/mdx-components.tsx:22`
- Improved image privacy/performance defaults with `loading="lazy"`, `decoding="async"`, and `referrerPolicy="no-referrer"`:
  - `components/mdx-components.tsx:25-33`

## Audit Notes

- Production dependency audit: `npm audit --omit=dev`
  - Result: `0 vulnerabilities`
- Pattern scan reviewed:
  - `dangerouslySetInnerHTML`
  - `innerHTML`
  - `outerHTML`
  - `insertAdjacentHTML`
  - `eval(`
  - `new Function`
  - `document.write`
  - `postMessage`
  - `NEXT_PUBLIC_`
  - `process.env`

