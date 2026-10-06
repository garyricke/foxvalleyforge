#!/usr/bin/env python3
"""Rebuild data/hours.json for the gated /hours page from the Time app.

Time (time.orbisdesign.com) holds every Clockify entry plus the ones logged
in the app itself, so it is the only source read here — adding Clockify on
top would double-count. Labels come from tools/hours-notes.json.

    python3 tools/build-hours.py

Needs TIME_API_KEY in ~/Documents/SOUL/.env. The key is never printed or written out.
"""
import json, math, os, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = 'Forge Maint 1'
BLOCK = {'hours': 50, 'rate': 80, 'price': 4000, 'opened': '2026-07-14'}


def env(path, key):
    for line in open(os.path.expanduser(path)):
        if line.startswith(key + '='):
            return line.split('=', 1)[1].strip().strip('"\'')
    raise SystemExit(f'{key} not found in {path}')


def quarter(minutes):
    """Nearest quarter hour, halves rounding up."""
    return math.floor(minutes / 15 + 0.5) / 4


def main():
    notes = json.load(open(os.path.join(ROOT, 'tools', 'hours-notes.json')))
    req = urllib.request.Request(
        f"https://time.orbisdesign.com/api/entries?since={BLOCK['opened']}",
        headers={'Authorization': 'Bearer ' + env('~/Documents/SOUL/.env', 'TIME_API_KEY')})
    raw = json.load(urllib.request.urlopen(req))

    include = set(notes['include'])
    entries, unlabeled = [], []
    for e in raw:
        if e['project_name'] != PROJECT and e['id'] not in include:
            continue
        label = notes['entries'].get(str(e['id']))
        if label is None:
            unlabeled.append(e['id'])
            label = ['site', e.get('summary') or e.get('note') or 'Site work']
        entries.append({'id': e['id'], 'date': e['day'], 'hours': quarter(e['minutes']),
                        'stream': label[0], 'desc': label[1]})
    entries.sort(key=lambda x: (x['date'], x['id']), reverse=True)

    adjustments = notes.get('adjustments', [])
    worked = sum(x['hours'] for x in entries)
    discount = -sum(a['hours'] for a in adjustments)
    used = worked - discount
    out = {'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
           'block': BLOCK, 'worked': worked, 'discount': discount, 'used': used,
           'remaining': BLOCK['hours'] - used,
           'streams': notes['streams'], 'adjustments': adjustments, 'entries': entries}
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data', 'hours.json'), 'w') as f:
        json.dump(out, f, indent=1)
        f.write('\n')

    print(f"{len(entries)} entries · {worked} h worked · {discount} h discount · {used} h used · {out['remaining']} h left")
    if unlabeled:
        print('No label yet (filed under site care, using the Time note):', unlabeled)


if __name__ == '__main__':
    main()
