# Launch checklist

Status of the standard "is this site launch-ready" checklist against this
app. Verified, not assumed — actual results, not a rubber stamp. Two
platform notes up front: (1) this is a single-page **tool**, not a content
or marketing site, so several content-site items don't apply by nature;
(2) it's hosted on **Streamlit Community Cloud**, which does not expose the
document `<head>`, static file root, or custom error pages to the app
author — several SEO/social items were technically blocked by the platform,
not skipped by choice, until a separate landing page was added (see below)
that covers them for free.

**Landing page:** https://huggingface.co/spaces/aadithya1234/ai-academic-assistant
— a static Hugging Face Space with a real `<head>` (title, meta description,
Open Graph image, favicon set), linking to the live Streamlit app. Built
because Streamlit Cloud can't serve these directly, and because this HF
account is on the free tier (Docker/Gradio/Streamlit Spaces need HF PRO for
`cpu-basic` compute — confirmed via a live test push, not assumed; static
Spaces are free and don't need compute).

## Do for basically any site

| Item | Status | Notes |
|---|---|---|
| Meta title per page | ✅ Done | `st.set_page_config(page_title=...)`; verified in a live browser - `<title>AI Academic Assistant</title>` |
| Meta description per page | ✅ Done, via landing page | Not possible on the Streamlit app itself (see platform note above). The HF Space landing page has a real `<meta name="description">`, verified live. |
| Favicon set | ✅ Done, via landing page | Streamlit app uses `page_icon="🎓"` (emoji, tab icon only). The landing page has a generated multi-size favicon set (16/32/180px PNG + .ico), verified live. |
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
| Robots.txt | ⛔ Blocked by platform | Still not possible on Streamlit Cloud (no static file root) or the HF static Space (single-page, not worth a crawl policy). Low value either way for a one-route tool. |
| Sitemap.xml | ⛔ Blocked by platform | Same as above; also low value - it's a one-route app, not a crawlable content site. |
| Open Graph image | ✅ Done, via landing page | Not possible on Streamlit Cloud directly. Generated a 1200×630 OG image and wired up `og:image`/`og:title`/`twitter:card` on the HF landing page - verified the image itself resolves with HTTP 200. Sharing the HF Space link (not the raw `.streamlit.app` link) now shows a proper card. |

## Conversion-design advice

| Item | Status | Notes |
|---|---|---|
| CTA above the fold | ✅ Already true | The question box + "Generate Answer" button *are* the entire page - there's nothing to scroll past. |
| Sticky mobile CTA | N/A | Applies to long scrolling pages with a persistent action bar; this page has no scroll depth for it to matter. |

## Remaining ⛔ items (robots.txt / sitemap.xml)

Low-value for a one-route tool either way, and fixing them for real means
self-hosting the Streamlit server behind your own reverse proxy (neither
Streamlit Cloud nor an HF static Space exposes a static file root) - a real
infrastructure change, not a code tweak. Not worth it unless this becomes a
multi-page, crawlable site.

## Note on the HF Space's live demo iframe

The landing page originally embedded the live Streamlit app via `<iframe>`.
It was removed before shipping: the Streamlit Cloud app was asleep at build
time (free-tier apps sleep after inactivity and gate behind a wake-up
screen), which would have shown visitors a broken embed instead of the
demo. The page links out to the app directly instead. Re-add the iframe
once the app is confirmed awake and working end-to-end if you want it.
