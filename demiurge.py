#!/usr/bin/env python3

import sys
import argparse
import datetime


def iso_to_datetime(iso):
    try:
        return datetime.datetime.strptime(iso, '%Y-%m-%d')
    except ValueError:
        print(f'Invalid date: {iso}', file=sys.stderr)
        sys.exit()
  

def extract_meeting_days(meeting_days_string):
    meeting_days = set()
    for c in meeting_days_string:
        try:
            meeting_days.add("MTWRFSU".index(c))
        except ValueError:
          print(f'Invalid day of the week {c}', file=sys.stderr)
    return meeting_days


def read_holidays(fn):
    holidays = set()
    with open(fn, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            holiday = iso_to_datetime(line)
            holidays.add(holiday)
    return holidays


def calculate_dates(start, end, days, holidays, dformat):
    dates = []
    date = start
    while date <= end:
        if date.weekday() in days and date not in holidays:
            dates.append(date.strftime(dformat))
        date = date + datetime.timedelta(days=1)
    return dates


def read_topics(dates):
    topics = [l.strip() for l in sys.stdin]
    topics += [''] * (dates - len(topics))
    return topics

def format_csv(table):
    return '\n'.join([','.join(row) for row in table])

def format_tex(table):
    table = list(table)
    cols = len(table[0])
    tex = '\\begin{tabular}{' + ('l' * cols) + '}\n'
    for row in table:
        tex += ' & '.join(row) + '\\\\\n'
    tex += '\\end{tabular}\n'
    return tex   

def format_html(table):
    table = list(table)
    cols = len(table[0])
    html = '<table>\n  <thead>\n    <tr>\n'
    html += '      <th></th>\n' * cols
    html += '    <tr>\n  </thead>\n  <tbody>\n'
    for row in table:
        html += '    <tr>\n'
        html += ''.join([f'      <td>{x}</td>\n' for x in row])
        html += '    </tr>\n'
    html += '  </tbody>\n</table>'
    return html

FORMAT = {
    'csv': lambda t: format_csv(t),
    'tex': lambda t: format_tex(t),
    'html': lambda t: format_html(t),
}

def format_data(dates, topics, columns, format):
    extra_columns = columns * [[''] * len(dates)]
    table = zip(dates, topics, *extra_columns)
    return FORMAT[format](table)


def main():
    parser = argparse.ArgumentParser(description='Generate a syllabus from basic parameters')
    parser.add_argument('-s', '--start-date', required=True, help='Start date')
    parser.add_argument('-e', '--end-date', required=True, help='End date')
    parser.add_argument('-d', '--meeting-days', required=True, help='Days class will meet (e.g. "MWF" or "TR")')
    parser.add_argument('-x', '--holidays', default='', help='File listing special days classes will not meet')
    parser.add_argument('-a', '--date-format', default='%d %b', help='Format for the date')
    parser.add_argument('-f', '--format', default='csv', help='Output format (csv, tex, html)')
    parser.add_argument('-c', '--columns', type=int, default=0, help='Number of extra columns to add')
    args = parser.parse_args()
    meeting_days = extract_meeting_days(args.meeting_days)
    start_date = iso_to_datetime(args.start_date)
    end_date = iso_to_datetime(args.end_date)
    holidays = set() if not args.holidays else read_holidays(args.holidays)
    meeting_dates = calculate_dates(start_date, end_date, meeting_days, holidays, args.date_format)
    topics = read_topics(len(meeting_dates))
    print(format_data(meeting_dates, topics, args.columns, args.format))
    
if __name__ == '__main__':
    main()