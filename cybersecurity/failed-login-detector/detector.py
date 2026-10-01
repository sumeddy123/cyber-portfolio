from collections import Counter
import re
import sys

FAILED_PATTERN = re.compile(
    r"Failed password.*from (?P<ip>\d+\.\d+\.\d+\.\d+)"
)

def analyze_log(path: str, threshold: int = 3):
    counts = Counter()

    with open(path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            match = FAILED_PATTERN.search(line)
            if match:
                counts[match.group("ip")] += 1

    print("Failed Login Summary")
    print("=" * 44)

    for ip, count in counts.most_common():
        status = "ALERT" if count >= threshold else "OK"
        print(f"{ip:15} {count:3} failed attempts  [{status}]")

    suspicious = {
        ip: count for ip, count in counts.items()
        if count >= threshold
    }

    print(f"\nSuspicious IPs: {len(suspicious)}")
    return suspicious

if __name__ == "__main__":
    log_path = sys.argv[1] if len(sys.argv) > 1 else "sample_auth.log"
    alert_threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    analyze_log(log_path, alert_threshold)
