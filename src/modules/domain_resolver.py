from typing import List
import dns.resolver

from src.modules.normalizer import domain_normalize


def resolve(domains: List[str]) -> dict[str, str]:
    domains = set(map(domain_normalize, domains))
    cnames = {}
    for domain in domains:
        try:
            response = dns.resolver.resolve(domain, 'A')
            cnames[domain] = domain_normalize(response.canonical_name)
        except dns.exception.DNSException:
            try:
                response = dns.resolver.resolve(domain, 'AAAA')
                cnames[domain] = domain_normalize(response.canonical_name)
            except dns.exception.DNSException:
                pass
    return cnames
