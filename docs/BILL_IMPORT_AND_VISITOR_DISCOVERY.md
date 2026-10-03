# Bill Import and Visitor Discovery

This document describes the two pre-evaluation product flows added to HelioSL.

## Authenticated electricity-bill import

1. A signed-in user opens **Energy > Import Bill**.
2. The user selects a text-based PDF, TXT or CSV electricity bill (maximum 5 MB).
3. HelioSL sends the file to `POST /api/v1/energy/me/bills/extract` using the user's JWT.
4. The backend extracts the provider, account reference, billing month, consumption, amount and meter readings where available.
5. HelioSL returns confidence and warnings. It does not retain the uploaded file.
6. The user reviews and edits the extracted month, kWh and amount.
7. Only after explicit confirmation does the frontend create a consumption record through the existing `/energy/me/consumption` endpoint.

The original document is not stored. The confirmation step prevents uncertain extraction from silently changing the user's energy history. The first release intentionally supports text-based files; scanned-image bills require a later OCR step.

Two fictional sample bills are available from the import screen:

- CEB household sample
- LECO business sample

They are synthetic test artifacts and must not be treated as real customer documents.

## First-visit Solar Path Finder

The public landing page includes a short discovery flow for visitors who are not ready to create an account.

1. The visitor chooses household or business.
2. The visitor selects a city; the website never requests live location.
3. The visitor provides a broad monthly-use band, goal and roof-access status.
4. HelioSL presents a preliminary scheme direction, a capacity band and a useful next step.
5. It also presents nearby provider leads from the official SLSEA registered-provider directory.
6. The visitor is encouraged to verify provider registration and current scheme terms before spending money, then can create an account or sign in.

The matcher is a discovery and lead-generation experience, not a quotation, current-tariff claim or engineering recommendation. Logged-in planning remains the correct place for calculations based on the user's own data.
