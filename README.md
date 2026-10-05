# KAY-KAY — LLM gateway

Small gateway demonstrating provider fallback, API-key hashing, conservative spend reservation, and telemetry. Provider implementations are deterministic stubs so the core is testable without an LLM account.

The budget is reserved before provider work; failed providers release the reservation; successful calls consume it. Issued API keys are required for gateway requests. This is a portfolio system, not a billing ledger or production authentication service.

## Run
`pip install -e . && uvicorn kaykay.app:app --reload`

## Test
`pytest -q`

## License
MIT.
