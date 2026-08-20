# Launch checklist

Status of the standard "is this site launch-ready" checklist against this
app. Verified, not assumed — actual results, not a rubber stamp. Two
platform notes up front: (1) this is a single-page **tool**, not a content
or marketing site, so several content-site items don't apply by nature;
(2) it's hosted on **Streamlit Community Cloud**, which does not expose the
document `<head>`, static file root, or custom error pages to the app
author — several SEO/social items are technically blocked by the platform,
not skipped by choice.

## Do for basically any site

| Item | Status | Notes |
|---|---|---|
| Meta title per page | ✅ Done | `st.set_page_config(page_title=...)`; verified in a live browser - `<title>AI Academic Assistant</title>` |
| Meta description per page | ⛔ Blocked by platform | Streamlit Cloud doesn't expose `<head>` to the app; there is no supported way to set `<meta name="description">`. Would need self-hosting behind a custom index.html. |
| Favicon set | 🟡 Partial | `page_icon="🎓"` sets the browser-tab icon (emoji, not a multi-size `.ico`/PNG set). Sufficient for a single-page tool; a full favicon set matters more for a multi-page/installable site. |
| Alt text on every image | N/A | The app renders no `<img>` elements (text + emoji only). |
| Mobile breakpoints | ✅ Verified | Tested at 375px width in a live browser: no horizontal overflow, inputs/button stack correctly (Streamlit's default responsive layout). |
| Compressed images | N/A | No images shipped. |
| Custom 404 page | N/A | Single-route app; there's no second page to 404 on, and Streamlit Cloud controls the error page for down/crashed apps. |
| Real contact address | ✅ Done | Footer now credits the author and links to the public GitHub repo (added a personal street/email address to a public repo isn't appropriate for this kind of project). |

## Do if the site has forms, accounts, or collects data

| Item | Status | Notes |
|---|---|---|
| Form error states | ✅ Done | Empty input → `st.warning`; over-length input is blocked at the input widget itself (`max_chars`) rather than surfaced as an error; API/parsing failures → `st.error`. Covered by tests in `tests/test_cli.py` / `test_prompt_layer.py` for the equivalent CLI path. |
| Loading states | ✅ Done | `st.spinner("Generating response...")` around the LLM call. |
| Thank you page | N/A | This isn't a lead-gen form with a submission flow - it's a synchronous Q&A tool; the "thank you" is the answer itself. |
| Privacy policy page | ✅ Done (lightweight) | Added an in-app "Privacy & data handling" expander disclosing that questions go to Groq's API and aren't stored, plus a link to Groq's own privacy policy. A full standalone policy page is disproportionate for a no-accounts, no-storage demo tool. |
| Terms page | ⏭️ Skipped, deliberately | No accounts, no payments, no user-generated content stored - there's no relationship to govern. Worth adding only if this ever takes real user accounts. |

## Situational

| Item | Status | Notes |
|---|---|---|
| Cookie banner | N/A | The app sets no cookies (Streamlit session state is server-side); no analytics installed either. Nothing to get consent for. |
| Analytics installed | ⏭️ Not installed | Deliberately skipped - wiring up GA/Plausible needs your account, and you didn't ask for tracking. Say the word if you want it. |
| Robots.txt | ⛔ Blocked by platform | No static file root is exposed on Streamlit Community Cloud. |
| Sitemap.xml | ⛔ Blocked by platform | Same as above; also low value - it's a one-route app, not a crawlable content site. |
| Open Graph image | ⛔ Blocked by platform | Same `<head>` limitation as meta description - can't set `og:image`/`og:title` on Streamlit Cloud. Sharing the link on LinkedIn/Twitter will show a generic/blank card. |

## Conversion-design advice

| Item | Status | Notes |
|---|---|---|
| CTA above the fold | ✅ Already true | The question box + "Generate Answer" button *are* the entire page - there's nothing to scroll past. |
| Sticky mobile CTA | N/A | Applies to long scrolling pages with a persistent action bar; this page has no scroll depth for it to matter. |

## If you want the ⛔ items fixed for real

The `<head>`-dependent items (meta description, OG image, robots.txt,
sitemap.xml) are only fixable by moving off Streamlit Community Cloud's
managed hosting to something that serves your own HTML shell - e.g. a
static landing page (with proper meta/OG tags) that links to or embeds the
Streamlit app, or self-hosting the Streamlit server behind your own
reverse proxy. That's a real infrastructure change, not a code tweak -
say if you want to scope it.
