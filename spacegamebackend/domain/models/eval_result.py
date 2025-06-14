class EvalResult:
    def __init__(self, result: bool, detail: str | None = None) -> None:  # noqa: FBT001
        self.result = result
        self.detail = detail

    def __bool__(self) -> bool:
        return self.result

    def __str__(self) -> str:
        return self.detail or ""

    def __add__(self, other: "EvalResult") -> "EvalResult":
        return EvalResult(self.result and other.result, f"{self} {other}")

    def __or__(self, other: "EvalResult") -> "EvalResult":
        if self.result or other.result:
            return EvalResult(True, None)
        return EvalResult(False, f"{self} {other}")

    def __ror__(self, other: "EvalResult") -> "EvalResult":
        if self.result or other.result:
            return EvalResult(True, None)
        return EvalResult(False, f"{self} {other}")

    def __repr__(self) -> str:
        return f"EvalResult(result={self.result}, detail={self.detail})"
