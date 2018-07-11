'''
Load DataONE ORE documents and output relations as a json dictionary, one entry per line.

'''

import sys
import os
import logging
import argparse
import dateparser
from pytz import timezone
from d1_client import cnclient_2_0
import json
import requests
from . import oreparser


PRODUCTION_CN = "https://cn.dataone.org/cn"
FORMAT_ID = "http://www.openarchives.org/ore/terms"

def textToDateTime(txt, default_tz='UTC'):
  logger = logging.getLogger('main')
  d = dateparser.parse(txt, settings={'RETURN_AS_TIMEZONE_AWARE': True})
  if d is None:
    logger.error("Unable to convert '%s' to a date time.", txt)
    return d
  if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
    logger.warning('No timezone information specified, assuming UTC')
    return d.replace(tzinfo = timezone('UTC'))
  return d


def getOREIdentifiers(client, pid):
  logger = logging.getLogger("getOREIdentifiers")
  logger.debug('Resolving %s', pid)
  ore_location = client.resolve(pid)
  url = ore_location.objectLocation[0].url
  logger.debug("Downloading from %s", url)
  #request = requests.get( url )
  ore = oreparser.OreParser()
  ore.deserialize(location=url)
  return ore.getRelations()


def main():
  parser = argparse.ArgumentParser(description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-l', '--log_level',
                      action='count',
                      default=0,
                      help='Set logging level, multiples for more detailed.')
  parser.add_argument('-x','--date_start',
                      default=None,
                      help="Starting time for listing")
  parser.add_argument('-y','--date_end',
                      default=None,
                      help="End time for listing")
  parser.add_argument('-b','--base_url',
                      default=PRODUCTION_CN,
                      help="Baseurl for listObjects ({})".format(PRODUCTION_CN))
  parser.add_argument('-C', '--max_records',
                      default=10,
                      help='Maximum number of entries to retrieve.')
  parser.add_argument('-p', '--page_size',
                      default=10,
                      help='Page size to return')
  parser.add_argument('-s', '--start_index',
                      default=0,
                      help='Zero based index of first entry')
  args = parser.parse_args()
  # Setup logging verbosity
  levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  level = levels[min(len(levels) - 1, args.log_level)]
  logging.basicConfig(level=level,
                      format="%(asctime)s %(levelname)s %(message)s")
  logger = logging.getLogger('main')
  date_start = None
  date_end = None
  if args.date_start is not None:
    date_start = textToDateTime(args.date_start)
    logger.info("date_start '%s' parsed as %s", args.date_start, str(date_start))
  if args.date_end is not None:
    date_end = textToDateTime(args.date_end)
    logger.info("date_end '%s' parsed as %s", args.date_end, str(date_end))
  client = cnclient_2_0.CoordinatingNodeClient_2_0(args.base_url, allow_redirects=False)
  start_index = args.start_index
  max_to_retrieve = int(args.max_records)
  total_records = -1
  counter = int(start_index)
  n_retrieved = 0
  while n_retrieved < max_to_retrieve:
    res = None
    kwparams = {'count':args.page_size,
                'start': start_index,
                'fromDate': date_start,
                'toDate': date_end,
                'formatId': FORMAT_ID
                }
    response = client.listObjects(**kwparams)
    if total_records < 0:
      logger.info("Total matching records = %d", response.total)
    if total_records < 0:
      total_records = int(response.total)
      if max_to_retrieve > total_records:
        max_to_retrieve = total_records
    n_retrieved += response.count
    logger.info("Retrieved: %d", n_retrieved)
    start_index = response.start + response.count
    for entry in response.objectInfo:
      ore_pid = entry.identifier.value().strip()
      relations = getOREIdentifiers(client, ore_pid)
      print(json.dumps(relations))


if __name__ == "__main__":
  sys.exit(main())