"""Offline authentication-log triage. Input is JSON Lines, never executable code."""
import argparse
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
import json
from pathlib import Path
import sys


def load_events(path):
    events = []
    with Path(path).open(encoding='utf-8') as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ValueError('expected a JSON object')
                timestamp = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                if timestamp.tzinfo is None:
                    raise ValueError('timestamp must include a timezone')
                ip = str(ip_address(item['source_ip']))
                user = item['username']
                if not isinstance(user, str) or not user.strip() or len(user) > 128:
                    raise ValueError('username must contain 1-128 characters')
                if item['outcome'] not in ('failure', 'success'):
                    raise ValueError('outcome must be failure or success')
                events.append(dict(timestamp=timestamp.astimezone(timezone.utc),
                                   source_ip=ip, username=user, outcome=item['outcome']))
            except (KeyError, TypeError, ValueError, AttributeError) as exc:
                raise ValueError(f'Invalid record on line {number}: {exc}') from exc
    # Stable ordering preserves input order when timestamps are identical.
    return sorted(events, key=lambda event: event['timestamp'])


def analyze(events, threshold=5, window_seconds=300):
    if threshold < 2 or window_seconds < 1:
        raise ValueError('threshold must be >= 2 and window_seconds must be >= 1')
    window = timedelta(seconds=window_seconds)
    failures = defaultdict(deque)
    last_alert = {}
    alerts = []
    for event in sorted(events, key=lambda item: item['timestamp']):
        now, ip = event['timestamp'], event['source_ip']
        recent = failures[ip]
        while recent and now - recent[0]['timestamp'] > window:
            recent.popleft()
        if event['outcome'] == 'failure':
            recent.append(event)
            if len(recent) >= threshold and (ip not in last_alert or now - last_alert[ip] >= window):
                alerts.append({'rule': 'repeated_failed_logins', 'severity': 'medium',
                               'timestamp': now.isoformat(), 'source_ip': ip,
                               'usernames': sorted({e['username'] for e in recent}),
                               'failure_count': len(recent)})
                last_alert[ip] = now
        else:
            matching = [e for e in recent if e['username'] == event['username']]
            if len(matching) >= threshold:
                alerts.append({'rule': 'success_after_repeated_failures', 'severity': 'high',
                               'timestamp': now.isoformat(), 'source_ip': ip,
                               'usernames': [event['username']], 'failure_count': len(matching)})
            # A success consumes that account's failures, avoiding duplicate success alerts.
            failures[ip] = deque(e for e in recent if e['username'] != event['username'])
    return {'events_processed': len(events), 'threshold': threshold,
            'window_seconds': window_seconds, 'alert_count': len(alerts), 'alerts': alerts}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--threshold', type=int, default=5)
    parser.add_argument('--window-seconds', type=int, default=300)
    parser.add_argument('--output', type=Path, help='JSON report path; defaults to stdout')
    args = parser.parse_args(argv)
    try:
        report = analyze(load_events(args.input), args.threshold, args.window_seconds)
        output = json.dumps(report, indent=2) + '\n'
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
