import re

_ZERO_END = r"\s*(?:;|\"|'|!|$)"
# Both conditions must sit inside one style="..." attribute, in either order.
_STYLE = r"style\s*=\s*([\"'])(?=(?:(?!\1).)*?{a})(?=(?:(?!\1).)*?{b})"
_WHITE = r"#fff(?:fff)?\b|white\b"

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (label, re.compile(rx, re.IGNORECASE | re.DOTALL))
    for label, rx in [
        ("ignore_previous_instructions", r"ignore\s+(all\s+)?(previous|prior)\s+instructions"),
        ("disregard_previous_instructions", r"disregard\s+(all\s+)?(previous|prior)\s+instructions"),
        ("ai_assistant_marker", r"ai\s+assistant\s*:"),
        ("css_display_none", r"display\s*:\s*none"),
        ("css_visibility_hidden", r"visibility\s*:\s*hidden"),
        ("css_font_size_zero", r"font-size\s*:\s*0(?:\.0+)?(?:px|pt|em|rem|%)?" + _ZERO_END),
        ("css_opacity_zero", r"opacity\s*:\s*0(?:\.0+)?" + _ZERO_END),
        (
            "css_offscreen",
            _STYLE.format(a=r"position\s*:\s*(?:absolute|fixed)", b=r"(?:left|top)\s*:\s*-\d{4,}"),
        ),
        (
            "css_white_on_white",
            _STYLE.format(
                a=rf"(?<!background-)color\s*:\s*(?:{_WHITE})",
                b=rf"background(?:-color)?\s*:\s*(?:{_WHITE})",
            ),
        ),
    ]
]


def check_injection(body: str) -> list[str]:
    return [f"hidden_instruction: {label}" for label, rx in _PATTERNS if rx.search(body)]
