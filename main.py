"""Emit the bundled passport spread image to the grading output slot.

The spread shows an Ostravian passport whose issuing state renamed itself
mid-validity; entry.png is rendered by render.py and copied verbatim here.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
TARGET = Path("/output/entry.png")
SIZE_LIMIT = 1_048_576  # 1 MiB


def main() -> None:
    payload = SOURCE.read_bytes()
    if len(payload) > SIZE_LIMIT:
        raise ValueError(f"entry.png is {len(payload)} bytes, over the 1 MiB limit")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)


if __name__ == "__main__":
    main()
