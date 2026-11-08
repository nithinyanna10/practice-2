def domain_matches(host: str, domain: str) -> bool:
    host, domain = host.lower(), domain.lower()
    return host == domain or host.endswith("." + domain)
