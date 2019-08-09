# Demiurge

Demiurge is a python script for automatically creating syllabi based on a relevant dates, meeting days, and a list of topics. It uses features of Python 3.6 and above (string interpolation) so it must be run with a recent Python 3 interpreter.

## Usage

It is most informative to start with a complete working example. To create a schedule for a class beginning on 26 Aug 2019, ending 06 Dec 2019, meeting on Mondays and Wednesdays, with holidays listed in holidays.txt and topics listed in hl4ai_topics.txt as a CSV file, issue the following command:

```shell
$ python demiurge.py -s 2019-08-26 -e 2019-12-06 -d MW -c 1 -x holidays.txt -f csv < hl4ai_topics.txt > schedule.csv
```

The “topics” file that the script takes as input (this cannot be omitted, but the file can be empty) contains a list—one per line—of lecture titles or class topics. These are aligned with the available dates. In output, the sequence of dates is never truncated but the sequence of topics will be truncated if there are not enough dates for all of them.

A complete list of options can be obtained by entering `python demiurge.py -h`:

```
Generate a syllabus from basic parameters

optional arguments:
  -h, --help            show this help message and exit
  -s START_DATE, --start-date START_DATE
                        Start date
  -e END_DATE, --end-date END_DATE
                        End date
  -d MEETING_DAYS, --meeting-days MEETING_DAYS
                        Days class will meet (e.g. "MWF" or "TR")
  -x HOLIDAYS, --holidays HOLIDAYS
                        File listing special days classes will not meet
  -a DATE_FORMAT, --date-format DATE_FORMAT
                        Format for the date
  -f FORMAT, --format FORMAT
                        Output format (csv, tex, html)
  -c COLUMNS, --columns COLUMNS
                        Number of extra columns to add
```

All dates must be entered in ISO formaat (YYY-MM-DD). The recognized days of the week are as follows:


| Day       | Code |
|-----------|------|
| Monday    | M    |
| Tuesday   | T    |
| Wednesday | W    |
| Thursday  | R    |
| Friday    | F    |
| Saturday  | S    |
| Sunday    | U    |

The “holidays” file must consist of a sequence of ISO dates, one per line.

In output, dates are formated using `strftime`. The `--format` option acceepts any format possible for `strftime`. For more information, see [the documentation](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior).