"""Copy the bundled passport image to the output location."""

from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target = Path("/output/entry.png")
    target.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    if len(data) > 1_048_576:
        raise ValueError("entry.png exceeds the 1 MiB limit")
    target.write_bytes(data)


if __name__ == "__main__":
    main()
