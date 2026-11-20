# Rent Receipt Generator — Self-hosted PDF generator, €9 one-time

Small landlords give tenants a receipt for rent paid. No account, no SaaS,
nothing leaves your machine.

## What it does

POST `/rent-receipt` with JSON → get a printable PDF rent receipt.

Fields: landlord name/address, tenant name, property address, amount,
rent period, date, payment method, optional note.

## Example

```bash
curl -X POST http://localhost:8021/rent-receipt \
  -H 'Content-Type: application/json' \
  -d '{"landlord_name":"Mary Smith","landlord_address":"123 Main St","tenant_name":"John Doe","property_address":"456 Oak Ave","amount":"1200","period":"January 2026","date":"2026-02-01","payment_method":"Check","note":""}' \
  -o rent-receipt.pdf
```

## How to run

```bash
python3 service.py
# then POST /rent-receipt as above
```

## Frontend

Open `frontend/index.html` in your browser for a fill-in-the-blanks form that
generates and downloads the PDF.

## License

€9 one-time. Download the ZIP, extract, run `python3 service.py`. Use it for as
many receipts as you like. Sold as-is — no account, no subscription, no per-use fee.
