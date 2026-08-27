def format_duration(value: int, decimals: int = 2) -> str:
    """
    Convert a duration from nanoseconds into the largest readable time unit.

    Examples:
        >>> format_duration(500)
        '500 ns'

        >>> format_duration(1_500)
        '1.5 μs'

        >>> format_duration(1_500_000)
        '1.5 ms'

        >>> format_duration(1_500_000_000)
        '1.5 s'

        >>> format_duration(90_000_000_000)
        '1.5 min'

        >>> format_duration(5_400_000_000_000)
        '1.5 hr'

    Args:
        value:
            Duration in nanoseconds.

        decimals:
            Maximum number of decimal places to display.

    Returns:
        A human-readable duration string.
    """

    if value < 0:
        raise ValueError("Duration must be non-negative")

    units = [
        ("ns", 1),
        ("μs", 1_000),
        ("ms", 1_000_000),
        ("s", 1_000_000_000),
        ("min", 60 * 1_000_000_000),
        ("hr", 60 * 60 * 1_000_000_000),
    ]

    size = float(value)
    unit_name = "ns"

    for name, factor in units:
        if value >= factor:
            unit_name = name
            size = value / factor

    formatted = f"{size:.{decimals}f}".rstrip("0").rstrip(".")

    return f"{formatted} {unit_name}"


def main() -> None:
    print("Hello from utils!")
