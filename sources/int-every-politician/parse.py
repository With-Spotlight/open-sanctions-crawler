import os
import sys
import json
import logging
import unicodecsv
from normality import slugify
from datetime import datetime

from peplib import Source
from peplib.util import make_id
from peplib.country import normalize_country

log = logging.getLogger(__name__)

PUBLISHER = {
    'publisher': 'EveryPolitician.org',
    'publisher_url': 'http://www.everypolitician.org/'
}


def parse_ts(ts):
    return datetime.fromtimestamp(int(ts)).date().isoformat()


def parse_politician(source, country, legislature, data):
    # from pprint import pprint
    # pprint(policitian)

    # TODO: add politician
    code = normalize_country(country.get('code'))
    entity = {
        'uid': make_id('evpo', data.get('id').split('-')[-1]),
        'name': data.get('name'),
        'type': 'individual',
        'addresses': [{'country': code}],
        'updated_at': parse_ts(legislature.get('lastmod')),
        'source_url': data.get('source_url'),
        'source': '%s (%s)' % (legislature['name'], country['name'])
    }
    entity.update(PUBLISHER)
    source.emit(entity)


def parse_politicians(data_dir, source, country, legislature, csv):
    _, csv = csv.split('data/', 1)
    with open(os.path.join(data_dir, csv), 'r') as fh:
        for row in unicodecsv.DictReader(fh):
            parse_politician(source, country, legislature, row)


def everypolitician_parse(data_dir):
    with open(os.path.join(data_dir, 'countries.json'), 'r') as fh:
        data = json.load(fh)

    for country in data:
        legs = country.pop('legislatures', [])
        for legislature in legs:
            legis = slugify(legislature['name'], sep='-')
            source_id = 'evpo-%s-%s' % (country['code'].lower(), legis)
            print 'Source', source_id
            source = Source(source_id)
            periods = legislature.pop('legislative_periods', [])
            for period in periods:
                parse_politicians(data_dir, source, country, legislature,
                                  period.get('csv'))

if __name__ == '__main__':
    everypolitician_parse(sys.argv[1])
