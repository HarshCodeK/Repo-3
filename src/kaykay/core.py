from dataclasses import dataclass
from threading import Lock
from typing import Callable


@dataclass
class Request:
    api_key: str
    model: str
    prompt: str
    max_tokens: int = 256


@dataclass
class Response:
    text: str
    provider: str
    estimated_cost: float


class Gateway:
    def __init__(self, providers: dict[str, Callable], prices: dict[str, float], budget: float = 1.0):
        self.providers = providers
        self.prices = prices
        self.budget = budget
        self.spent = 0.0
        self.reserved = 0.0
        self.usage = []
        self._lock = Lock()

    def estimate(self, request: Request) -> float:
        return max(1, len(request.prompt.split()) + request.max_tokens) / 1000 * self.prices.get(request.model, 0.002)

    def complete(self, request: Request) -> Response:
        reservation = self.estimate(request)
        with self._lock:
            if self.spent + self.reserved + reservation > self.budget:
                raise RuntimeError("budget_exceeded")
            self.reserved += reservation

        try:
            errors = []
            for name, call in self.providers.items():
                try:
                    text = call(request)
                    with self._lock:
                        self.reserved -= reservation
                        self.spent += reservation
                        self.usage.append({"provider": name, "model": request.model, "cost": reservation})
                    return Response(text, name, reservation)
                except Exception:
                    errors.append(name)
            raise RuntimeError("all_providers_failed: " + ", ".join(errors))
        finally:
            with self._lock:
                if reservation > 0 and self.reserved >= reservation and not any(
                    entry["model"] == request.model and entry["cost"] == reservation
                    for entry in self.usage
                ):
                    self.reserved -= reservation
