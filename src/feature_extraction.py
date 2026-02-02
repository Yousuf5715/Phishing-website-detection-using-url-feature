import re
import tldextract

SUSPICIOUS_KEYWORDS = [
    "secure", "account", "update", "login", "verify", "bank", "webscr", "confirm",
    "password", "signin", "ebayisapi", "paypal", "invoice", "free", "lucky"
]

IP_REGEX = re.compile(r"^(?:http[s]?://)?\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?(?:/.*)?$")


def has_ip(url: str) -> int:
    return int(bool(IP_REGEX.match(url)))


def count_digits(s: str) -> int:
    return sum(c.isdigit() for c in s)


def extract_domain(url: str) -> str:
    e = tldextract.extract(url)
    if e.subdomain:
        return ".".join(p for p in (e.subdomain, e.domain, e.suffix) if p)
    return ".".join(p for p in (e.domain, e.suffix) if p)


def extract_features(url: str):
    """Return a list of numerical features extracted from a URL in fixed order.

    Features (order):
    - url_length
    - host_length
    - count_dots
    - count_hyphens
    - count_digits
    - has_ip (0/1)
    - has_https (0/1)
    - count_at ("@" occurrences)
    - redirection (1 if suspicious else 0)
    - susp_word (count of suspicious keywords present)
    """
    u = url.strip()
    url_length = len(u)
    domain = extract_domain(u)
    host_length = len(domain)
    count_dots = u.count('.')
    count_hyphens = u.count('-')
    digits = count_digits(u)
    ip = has_ip(u)
    has_https = int(u.lower().startswith('https'))
    count_at = u.count('@')

    # redirection: check for an extra '//' after the protocol
    redir = 0
    try:
        first_double = u.find('//')
        if first_double != -1:
            later = u.find('//', first_double + 2)
            if later != -1:
                redir = 1
    except Exception:
        redir = 0

    # suspicious keywords
    low = u.lower()
    susp_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in low)

    return [
        url_length,
        host_length,
        count_dots,
        count_hyphens,
        digits,
        ip,
        has_https,
        count_at,
        redir,
        susp_count,
    ]


FEATURE_NAMES = [
    "url_length",
    "host_length",
    "count_dots",
    "count_hyphens",
    "count_digits",
    "has_ip",
    "has_https",
    "count_at",
    "redirection",
    "suspicious_keyword_count",
]


if __name__ == '__main__':
    # quick smoke test
    tests = [
        "http://192.168.0.1/login",
        "https://secure-paypal.com/confirm",
        "https://www.google.com",
        "http://example.com/@username",
    ]
    for t in tests:
        print(t, extract_features(t))
