"""
Step 4 — Guardrails AI Validators
====================================
TASK:
  1. Build a PIIDetector validator that detects & redacts emails, phone
     numbers, SSNs, and credit card numbers
  2. Build a JSONFormatter validator that auto-repairs malformed JSON
  3. Wrap each with a Guard and test with sample inputs
  4. Run a full demo with 6 PII cases and 5 JSON cases

DELIVERABLE: All test cases pass (PII redacted, JSON repaired)

KEY CONCEPTS:
  - @register_validator -- declares a custom validator class
  - Validator.validate() -- implement the check + fix logic
  - OnFailAction.FIX -- replace output instead of raising an error
  - Guard().use(MyValidator(on_fail=...)) -- attach validator to guard
  - guard.validate(text) -> ValidationOutcome
    .validation_passed -- bool
    .validated_output   -- the (possibly repaired) output string

IMPORTANT: pass `on_fail` to the VALIDATOR constructor, NOT to Guard.use()
    WRONG: Guard().use(PIIDetector, on_fail=OnFailAction.FIX)  <- TypeError
    RIGHT: Guard().use(PIIDetector(on_fail=OnFailAction.FIX))  <- correct
"""

import re
import json

# ── 1. Imports ───────────────────────────────────────────────────────────────
# Guardrails AI thay doi import path giua cac phien ban.
# Thu nhieu path de tuong thich.
try:
    from guardrails import Guard
    from guardrails.validators import (
        Validator,
        register_validator,
        OnFailAction,
        PassResult,
        FailResult,
    )
except ImportError:
    try:
        from guardrails import Guard
        from guardrails.validator_base import (
            Validator,
            register_validator,
            OnFailAction,
            PassResult,
            FailResult,
        )
    except ImportError:
        from guardrails import Guard, OnFailAction
        from guardrails.validator_base import Validator, register_validator
        from guardrails.validators import PassResult, FailResult


# ── 2. PII Detector Validator ─────────────────────────────────────────────────
@register_validator(name="custom/pii-detector", data_type="string")
class PIIDetector(Validator):
    """
    Detects and redacts Personally Identifiable Information (PII).

    Patterns detected:
      - EMAIL:       xxx@xxx.xxx
      - PHONE:       (123) 456-7890 or 123-456-7890
      - SSN:         123-45-6789
      - CREDIT_CARD: 1234 5678 9012 3456 (hoac dashes)
    """

    PII_PATTERNS = {
        "EMAIL":       r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PHONE":       r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
        "SSN":         r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    }

    def validate(self, value: str, metadata: dict):
        """
        Quet PII trong value, redact tat ca neu tim thay.

        Steps:
          1. Copy value -> redacted_text
          2. Voi moi PII type va pattern:
             - Tim tat ca matches
             - Thay the bang [PII_TYPE_REDACTED]
             - Ghi lai vao found_pii
          3. Neu co PII -> PassResult(value_override=redacted_text)
          4. Khong co   -> PassResult(value_override=value)

        Luon tra PassResult (khong FailResult) vi muc tieu la redact,
        khong phai chan request.
        """
        redacted_text = value
        found_pii     = []

        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, value)
            for match in matches:
                redacted_text = redacted_text.replace(match, f"[{pii_type}_REDACTED]")
                found_pii.append((pii_type, match))

        if found_pii:
            print(f"  WARNING: Redacted {len(found_pii)} PII item(s): {[p[0] for p in found_pii]}")
            return PassResult(value_override=redacted_text)

        return PassResult(value_override=value)


# ── 3. JSON Formatter Validator ───────────────────────────────────────────────
@register_validator(name="custom/json-formatter", data_type="string")
class JSONFormatter(Validator):
    """
    Validates and auto-repairs malformed JSON strings.

    Common repairs:
      - Strip markdown code fences (``` or ```json)
      - Replace single quotes with double quotes
      - Remove trailing commas before } or ]
      - Re-serialize with json.dumps for consistent formatting
    """

    @staticmethod
    def _repair(text: str) -> str:
        """
        Thu sua JSON malformed.

        Steps:
          1. Strip whitespace
          2. Bo markdown fences (```json...``` hoac ```...```)
          3. Single quotes -> double quotes
          4. Xoa trailing commas truoc } hoac ]
        """
        text = text.strip()

        # Bo markdown code fences
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$',          '', text)
        text = text.strip()

        # Single quotes -> double quotes
        text = text.replace("'", '"')

        # Xoa trailing commas (`,}` hoac `,]`)
        text = re.sub(r',\s*([}\]])', r'\1', text)

        return text

    def validate(self, value: str, metadata: dict):
        """
        Thu parse JSON truc tiep.
        Neu that bai, chay _repair() roi thu lai.

        - Thanh cong  -> PassResult(value_override=json.dumps(parsed, indent=2))
        - That bai    -> FailResult voi fix_value la JSON error object
        """
        # Buoc 1: thu parse truc tiep
        try:
            parsed  = json.loads(value)
            repaired = json.dumps(parsed, indent=2)
            return PassResult(value_override=repaired)
        except json.JSONDecodeError:
            pass

        # Buoc 2: thu repair roi parse lai
        try:
            repaired_text = self._repair(value)
            parsed        = json.loads(repaired_text)
            repaired      = json.dumps(parsed, indent=2)
            print("  INFO: JSON repaired successfully")
            return PassResult(value_override=repaired)
        except json.JSONDecodeError as e:
            error_json = json.dumps({
                "error": "invalid_json",
                "detail": str(e),
                "raw": value[:200],
            })
            return FailResult(
                error_message=f"Invalid JSON after repair attempt: {e}",
                fix_value=error_json,
            )


# ── 4. PII Guard demo ────────────────────────────────────────────────────────
def demo_pii_guard():
    """
    Test PIIDetector voi 6 cases:
      1. Email
      2. Phone
      3. SSN
      4. Credit card
      5. Multiple PII in one text
      6. Clean text (no PII)
    """
    print("\n" + "=" * 55)
    print("  PII Detection Demo")
    print("=" * 55)

    guard = Guard().use(PIIDetector(on_fail=OnFailAction.FIX))

    test_cases = [
        ("Email",       "Contact John at john.doe@example.com for details."),
        ("Phone",       "Call our support line at (555) 867-5309."),
        ("SSN",         "Patient SSN is 123-45-6789 on file."),
        ("Credit Card", "Payment made with card 4532 1234 5678 9010."),
        ("Multi-PII",   "Email: alice@example.com, Phone: 555-123-4567"),
        ("Clean",       "No sensitive information in this text."),
    ]

    for label, text in test_cases:
        result = guard.validate(text)
        status = "REDACTED" if result.validated_output != text else "CLEAN"
        print(f"\n[{label}] -> {status}")
        print(f"  Input : {text}")
        print(f"  Output: {result.validated_output}")


# ── 5. JSON Guard demo ────────────────────────────────────────────────────────
def demo_json_guard():
    """
    Test JSONFormatter voi 5 cases:
      1. Valid JSON (pass as-is)
      2. JSON voi markdown fences (strip va pass)
      3. JSON voi single quotes (chuyen sang double quotes)
      4. JSON voi trailing comma (xoa va pass)
      5. Truly invalid JSON (fail cleanly)
    """
    print("\n" + "=" * 55)
    print("  JSON Formatting Demo")
    print("=" * 55)

    guard = Guard().use(JSONFormatter(on_fail=OnFailAction.FIX))

    test_cases = [
        ("Valid JSON",      '{"name": "Alice", "age": 30}'),
        ("Markdown fences", '```json\n{"name": "Bob", "role": "admin"}\n```'),
        ("Single quotes",   "{'name': 'Charlie', 'score': 95}"),
        ("Trailing comma",  '{"key": "value", "items": [1, 2, 3,]}'),
        ("Truly invalid",   "This is not JSON at all: ??? {]"),
    ]

    for label, text in test_cases:
        result = guard.validate(text)
        status = "Pass" if result.validation_passed else "Fail"
        print(f"\n[{label}] -> {status}")
        print(f"  Input : {text[:70]}")
        print(f"  Output: {str(result.validated_output)[:70]}")


# ── 6. Main ─────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  Step 4: Guardrails AI Validators")
    print("=" * 55)

    demo_pii_guard()
    demo_json_guard()

    print("\n" + "=" * 55)
    print("  Step 4 complete!")
    print("  Save logs:")
    print("    python 04_guardrails_validator.py | tee evidence/04_pii_demo_log.txt")
    print("=" * 55)


if __name__ == "__main__":
    main()
