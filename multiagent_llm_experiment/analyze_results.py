"""Recreate a summary and an SVG bar chart from raw protocol-v2 rows."""
import argparse
import csv
from html import escape
from pathlib import Path

from metrics import summarize, write_summary_from_raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()
    with args.raw.open(newline="", encoding="utf-8") as stream:
        rows = summarize(list(csv.DictReader(stream)))
    write_summary_from_raw(args.raw, args.summary)
    height = 60 + 40 * len(rows)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="{height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<text x="10" y="20" font-family="sans-serif">Success rate among eligible runs</text>']
    for index, row in enumerate(rows):
        y = 40 + index * 40
        label = escape(f'{row["architecture"]} ({row["model"]})')
        rate = row["success_rate"]
        svg.append(f'<text x="10" y="{y + 14}" font-family="sans-serif" font-size="12">{label}</text>')
        if rate != "":
            svg.append(f'<rect x="260" y="{y}" width="{400 * rate:.2f}" height="18" fill="#3968a4"/>')
            svg.append(f'<text x="{265 + 400 * rate:.2f}" y="{y + 14}" font-family="sans-serif" font-size="12">{rate:.0%}</text>')
    svg.append("</svg>")
    with args.plot.open("x", encoding="utf-8") as stream:
        stream.write("\n".join(svg) + "\n")


if __name__ == "__main__":
    main()
