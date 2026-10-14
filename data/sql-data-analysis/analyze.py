"""Reproducible, in-memory SQL security analytics with synthetic fixtures."""
import argparse
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent


def report(threshold=3):
    if threshold < 1:
        raise ValueError('threshold must be positive')
    connection = sqlite3.connect(':memory:')
    connection.row_factory = sqlite3.Row
    try:
        for name in ('schema.sql', 'sample.sql'):
            connection.executescript((ROOT / name).read_text(encoding='utf-8'))
        queries = (ROOT / 'queries.sql').read_text(encoding='utf-8').split('-- Named query: ')[1:]
        result = {}
        for block in queries:
            name, sql = block.split('\n', 1)
            result[name.strip()] = [dict(row) for row in connection.execute(sql, {'threshold': threshold})]
        return result
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--threshold', type=int, default=3)
    args = parser.parse_args()
    if args.threshold < 1:
        parser.error('threshold must be positive')
    print(json.dumps(report(args.threshold), indent=2))


if __name__ == '__main__':
    main()
