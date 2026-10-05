# KAY-KAY — LLM gateway

Small gateway demonstrating provider fallback, API-key hashing, conservative spend reservation, and telemetry. Provider implementations are deterministic stubs so the core is testable without an LLM account.

The budget is checked before provider work; failed providers fall through; successful calls consume one reservation. This is a portfolio system, not a billing ledger or production authentication service.

## Run
`pip install -e . && uvicorn kaykay.app:app --reload`

## Test
`pytest -q`

## License
MIT.
