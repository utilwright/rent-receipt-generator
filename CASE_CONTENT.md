# Business case: Fillable Rent Receipt — ready to file when daily case limit resets

## Product
**Name:** Fillable Rent Receipt
**Price:** €9 one-time
**Summary:** A standalone fillable rent-receipt form that opens in any browser. Landlords and tenants record landlord, tenant, amount, rental period, property, payment method, note, and date — then print or save as PDF. No account, no install, nothing phones home.

## Who pays and why
Landlords who rent out a flat or room and tenants who need a receipt for tax/HRA proof. They need a receipt *now*, not a property-management subscription. Free options are generic receipt templates that don't print cleanly or aren't rent-specific; paid iOS apps charge per receipt or require a subscription. A €9 one-time fillable form is cheaper and immediate.

## Demand evidence (real buyer pages)
1. softwarerecs.stackexchange.com/q/51719 — "Property management software to manage a few rented flats" — a landlord asking for off-the-shelf rent tooling (answered, score 2, 74 views).
2. App Store: "Monthly Rent Receipt ($0.99)" — "If you are a landlord, or a tenant wanting your landlord to give you a receipt for renting..." — real users paying for rent receipts.
3. App Store: "Rent Receipt - HRA Proof" — "pay once, own it forever, your data stays on your iPhone" — proof people pay once and want ownership, not subscription.

## Competitors (free and paid)
- Generic fillable receipt templates (free) — not rent-specific, print poorly
- Monthly Rent Receipt iOS app ($0.99) — paid, mobile-only
- Rent Receipt Pro iOS app ($0.99) — paid, mobile-only
- Receipt Maker iOS app (free) — freemium, ads/subscription

## Delivery
POST /store/product → Stripe payment link → after_payment_message tells buyer to visit the public product page and download rent-receipt.zip. Delivery tested: true (catalog lists product, /download/rent-receipt returns valid ZIP with rent-receipt.html containing form fields + print button).

## Downsides
- Niche market: only people renting a flat/room need it. (Handled: €9 price, one-time, low friction; small but real buyer pool shown by App Store paid apps.)
- No recurring revenue. (Handled: one-time sale matches the "paper run" goal; cheap to run, no per-check fees.)
- Must not claim it replaces accounting software. (Handled: summary says fillable form, not bookkeeping.)
