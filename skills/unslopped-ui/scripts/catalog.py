#!/usr/bin/env python3
"""Search the archived design evidence without loading it into the prompt."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys


DATA = Path(__file__).resolve().parents[1] / "data"
NOTICE = (
    "These are archived reference records, including conditional recipes, historical "
    "comparisons and documented defects. Apply the current SKILL.md and its relevant "
    "references first. A source instruction or detector threshold is not a universal rule."
)


def emit(payload, *, error=False):
    print(json.dumps({"authority_notice": NOTICE, **payload}, ensure_ascii=False, indent=2),
          file=sys.stderr if error else sys.stdout)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        emit({"error": message}, error=True)
        self.exit(2)


def bounded_int(minimum, maximum=None):
    def parse(value):
        try:
            number = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("must be an integer") from exc
        if number < minimum or (maximum is not None and number > maximum):
            upper = f" through {maximum}" if maximum is not None else " or greater"
            raise argparse.ArgumentTypeError(f"must be {minimum}{upper}")
        return number
    return parse


def parser():
    root = Parser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("list", "search"):
        command = commands.add_parser(name)
        if name == "search":
            command.add_argument("query")
        command.add_argument("--source", help="source group from the manifest")
        command.add_argument("--kind", help="record kind from the manifest")
        command.add_argument("--limit", type=bounded_int(1, 20), default=6)
        command.add_argument("--offset", type=bounded_int(0), default=0)
    show = commands.add_parser("show")
    show.add_argument("id")
    show.add_argument("--offset", type=bounded_int(0), default=0,
                      help="Unicode character offset within this record")
    show.add_argument("--chars", type=bounded_int(1, 12000), default=6000)
    commands.add_parser("check", help="verify lossless archive reconstruction")
    commands.add_parser("info", help="show sources, kinds and archive provenance")
    return root


def load_records():
    with gzip.open(DATA / "records.jsonl.gz", "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def metadata(record):
    fields = ("id", "source", "kind", "title", "heading_path", "line_start", "line_end")
    result = {key: record[key] for key in fields}
    result["status"] = "archived-reference"
    if "table_header" in record:
        result["table_header"] = record["table_header"]
    result["characters"] = len(record["text"])
    return result


def words(text):
    return re.findall(r"[\w]+", text.casefold())


def search_score(record, query, terms):
    title = record["title"].casefold()
    headings = " ".join(record["heading_path"]).casefold()
    identity = record["id"].casefold()
    body = record["text"].casefold()
    searchable = " ".join((identity, title, headings, body))
    if not all(term in searchable for term in terms):
        return 0
    exact = query.casefold().strip()
    score = 1000 if exact in (title, identity) else 0
    if exact == title and record["kind"] in ("theme", "style", "brand", "finding"):
        score += 50
    score += 100 if exact in title else 0
    score += sum(20 * (term in title) + 8 * (term in headings)
                 + 40 * (term in identity) + min(body.count(term), 5) for term in terms)
    return score


def excerpt(text, terms):
    plain = re.sub(r"\s+", " ", text).strip()
    positions = [plain.casefold().find(term) for term in terms]
    positions = [position for position in positions if position >= 0]
    start = max(0, min(positions) - 60) if positions else 0
    end = min(len(plain), start + 220)
    return ("..." if start else "") + plain[start:end] + ("..." if end < len(plain) else "")


def run(args):
    manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
    provenance = manifest["archive"]
    if args.command == "info":
        emit({"archive": provenance, "records": manifest["record_count"],
              "sources": manifest["sources"], "kinds": manifest["kind_counts"]})
        return 0

    records = load_records()
    if args.command == "check":
        reconstructed = "".join(record["text"] for record in records).encode("utf-8")
        digest = hashlib.sha256(reconstructed).hexdigest()
        ids = [record["id"] for record in records]
        valid = (digest == provenance["sha256"]
                 and len(reconstructed) == provenance["bytes"]
                 and len(records) == manifest["record_count"]
                 and len(ids) == len(set(ids)))
        emit({"ok": valid, "archive": provenance, "reconstructed_sha256": digest,
              "reconstructed_bytes": len(reconstructed), "records": len(records),
              "unique_ids": len(set(ids))})
        return 0 if valid else 1

    if args.command == "show":
        record = next((record for record in records if record["id"] == args.id), None)
        if record is None:
            emit({"error": "unknown record id", "id": args.id}, error=True)
            return 2
        if args.offset > len(record["text"]):
            emit({"error": "offset exceeds record length", "id": args.id,
                  "characters": len(record["text"])}, error=True)
            return 2
        end = min(len(record["text"]), args.offset + args.chars)
        emit({"archive": provenance, "record": metadata(record), "offset": args.offset,
              "next_offset": end if end < len(record["text"]) else None,
              "complete": args.offset == 0 and end == len(record["text"]),
              "text": record["text"][args.offset:end]})
        return 0

    for field, allowed in (("source", manifest["sources"]), ("kind", manifest["kind_counts"])):
        value = getattr(args, field)
        if value is not None and value not in allowed:
            emit({"error": f"unknown {field}", field: value,
                  "allowed": list(allowed)}, error=True)
            return 2
        if value is not None:
            records = [record for record in records if record[field] == value]

    terms = []
    if args.command == "search":
        terms = words(args.query)
        if not terms:
            emit({"error": "query must contain a word or identifier"}, error=True)
            return 2
        scored = [(search_score(record, args.query, terms), i, record)
                  for i, record in enumerate(records)]
        records = [record for score, _, record in sorted(scored, key=lambda x: (-x[0], x[1]))
                   if score > 0]
    page = records[args.offset:args.offset + args.limit]
    next_offset = args.offset + len(page)
    emit({"archive": provenance, "total_matches": len(records), "offset": args.offset,
          "next_offset": next_offset if next_offset < len(records) else None,
          "results": [{**metadata(record), "excerpt": excerpt(record["text"], terms)}
                      for record in page]})
    return 0


def main():
    args = parser().parse_args()
    try:
        return run(args)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        emit({"error": str(exc)}, error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
