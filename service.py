#!/usr/bin/env python3
"""Rent Receipt Generator — self-hosted PDF rent receipt generator.

Endpoints:
  GET  /health   -> health check
  GET  /         -> frontend dashboard HTML
  POST /rent-receipt -> generates a signed rent receipt PDF (body: JSON)
"""
import os
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8010"))


def esc(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def generate_pdf(d):
    """Build a compact PDF rent receipt."""
    landlord = esc(d.get("landlord_name", ""))
    landlord_addr = esc(d.get("landlord_address", ""))
    tenant = esc(d.get("tenant_name", ""))
    tenant_addr = esc(d.get("tenant_address", ""))
    property_ = esc(d.get("property", ""))
    amount = esc(d.get("amount", ""))
    date = esc(d.get("date", ""))
    method = esc(d.get("method", ""))
    period = esc(d.get("period", ""))
    note = esc(d.get("note", ""))
    received_by = esc(d.get("received_by", landlord))

    lines = [
        "BT /F1 14 Tf 72 740 Td (RENT RECEIPT) Tj ET",
        "BT /F1 10 Tf 72 705 Td (This receipt acknowledges payment of rent for the property described below.) Tj ET",
        "BT /F1 10 Tf 72 675 Td (Landlord:) Tj ET",
        "BT /F1 10 Tf 120 675 Td (%s, %s) Tj ET" % (landlord, landlord_addr),
        "BT /F1 10 Tf 72 645 Td (Tenant:) Tj ET",
        "BT /F1 10 Tf 120 645 Td (%s, %s) Tj ET" % (tenant, tenant_addr),
        "BT /F1 10 Tf 72 615 Td (Property:) Tj ET",
        "BT /F1 10 Tf 120 615 Td (%s) Tj ET" % property_,
        "BT /F1 10 Tf 72 585 Td (Amount paid:) Tj ET",
        "BT /F1 10 Tf 130 585 Td (%s) Tj ET" % amount,
        "BT /F1 10 Tf 72 555 Td (Date of payment:) Tj ET",
        "BT /F1 10 Tf 145 555 Td (%s) Tj ET" % date,
        "BT /F1 10 Tf 72 525 Td (Payment method:) Tj ET",
        "BT /F1 10 Tf 140 525 Td (%s) Tj ET" % method,
        "BT /F1 10 Tf 72 495 Td (Rental period:) Tj ET",
        "BT /F1 10 Tf 135 495 Td (%s) Tj ET" % period,
    ]
    if note:
        lines += ["BT /F1 10 Tf 72 465 Td (Note:) Tj ET",
                  "BT /F1 10 Tf 100 465 Td (%s) Tj ET" % note]
    lines += [
        "BT /F1 10 Tf 72 405 Td (Received by:) Tj ET",
        "BT /F1 10 Tf 130 405 Td (%s) Tj ET" % received_by,
        "BT /F1 10 Tf 72 380 Td (Signature: ______________________ Date: __________) Tj ET",
        "BT /F1 10 Tf 72 355 Td (Tenant copy — keep for your records.) Tj ET",
    ]
    body = "\n".join(lines) + "\n"
    body_bytes = body.encode("latin-1", "replace")
    blen = len(body_bytes)

    def preamble():
        return ("%PDF-1.4\n"
                "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
                "4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
                "5 0 obj\n<< /Length %d >>\nstream\n" % blen)

    out = preamble().encode("latin-1") + body_bytes + b"\nendstream\nendobj\n"
    out += b"xref\n0 6\n0000000000 65535 f \n"
    # build xref offsets
    # compute offset of each object by reconstructing preamble length
    pre = len(preamble().encode("latin-1"))
    offs = [0, 9, pre, pre + len(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n") + len("2 0 obj\n"),
            0, 0]
    # simpler: write offsets after building full stream-less skeleton
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, json.dumps({"status": "ok", "service": "rent-receipt-generator"}), "application/json")
        elif self.path == "/":
            try:
                html = open("/work/rent-receipt-generator/frontend/index.html").read()
            except Exception:
                html = "<h1>Rent Receipt Generator</h1><p>Frontend not found.</p>"
            self._send(200, html, "text/html")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            d = json.loads(raw.decode()) if raw else {}
        except Exception:
            d = {}
        if self.path == "/rent-receipt":
            pdf = generate_pdf(d)
            self._send(200, pdf, "application/pdf")
        else:
            self._send(404, "not found", "text/plain")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
