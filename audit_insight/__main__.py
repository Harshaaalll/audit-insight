"""Allow ``python -m audit_insight`` to run the CLI pipeline."""

from audit_insight.pipeline import _cli

if __name__ == "__main__":
    _cli()
