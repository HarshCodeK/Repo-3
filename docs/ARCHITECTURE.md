# Architecture

Request policy is separated from HTTP transport. Cost is reserved before provider work; fallback handles provider failure; successful calls append telemetry. The in-memory budget is intentionally single-process. Durable multi-worker accounting requires transactional persistent storage.
