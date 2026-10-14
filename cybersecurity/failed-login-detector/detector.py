"""Count failed SSH logins by valid IPv4/IPv6 address in an offline log."""
import argparse
from collections import Counter
from ipaddress import ip_address
import json
from pathlib import Path
import re
import sys

FAILED_PATTERN = re.compile(r'Failed password.*? from (?P<ip>\S+)')


def summarize(path, threshold=3):
    if threshold < 1:
        raise ValueError('threshold must be positive')
    counts = Counter()
    invalid_addresses = 0
    with Path(path).open(encoding='utf-8') as source:
        for line in source:
            match = FAILED_PATTERN.search(line)
            if match:
                try:
                    address = str(ip_address(match.group('ip')))
                except ValueError:
                    invalid_addresses += 1
                    continue
                counts[address] += 1
    ordered = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    return {'threshold': threshold, 'failed_attempts': sum(counts.values()),
            'invalid_addresses': invalid_addresses, 'counts': ordered,
            'suspicious': {ip: count for ip, count in ordered.items() if count >= threshold}}


def analyze_log(path, threshold=3):
    report = summarize(path, threshold)
    print(json.dumps(report, indent=2))
    return report['suspicious']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path,
                        default=Path(__file__).with_name('sample_auth.log'))
    parser.add_argument('threshold', nargs='?', type=int, default=3)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        output = json.dumps(summarize(args.input, args.threshold), indent=2) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding='utf-8')
        else:
            print(output, end='')
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
