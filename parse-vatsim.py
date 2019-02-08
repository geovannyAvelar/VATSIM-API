import urllib2
import schedule
import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_vatsim_data(uri):
    request = urllib2.urlopen(uri)
    if request.getcode() == 200:
        return request.read()

    return ""

def parse_row(row):
    fields = row.split(':')

    row_dict = {}

    row_dict['callsign'] = fields[0]
    row_dict['cid'] = fields[1]
    row_dict['real_name'] = fields[2]
    row_dict['client_type'] = fields[3]
    row_dict['latitude'] = fields[5]
    row_dict['longitude'] = fields[6]

    if 'ATC' in row_dict['client_type']:
        row_dict['frequency'] = fields[4]

    if 'PILOT' in row_dict['client_type']:
        row_dict['altitude'] = fields[7]
        row_dict['ground_speed'] = fields[8]
        row_dict['planned_aircraft'] = fields[9]
        row_dict['planned_tascruise'] = fields[10]
        row_dict['planned_depairport'] = fields[11]
        row_dict['planned_altitude'] = fields[12]
        row_dict['planned_destairport'] = fields[13]
        row_dict['transponder'] = fields[17]
        row_dict['heading'] = fields[38]
    
    row_dict['server'] = fields[14]
    row_dict['protrevision'] = fields[15]
    row_dict['rating'] = fields[16]

    return row_dict

def parse_data(data):
    rows = data.split('\n')

    online_users = []

    for row in rows:
        if ':PILOT:' in row or ':ATC:' in row:
            online_users.append(parse_row(row))

    return online_users

def run():
    print "Running..."
    data = get_vatsim_data('http://vatsim-data.hardern.net/vatsim-data.txt')
    online = parse_data(data)

    for user in online:
        hash_name = "vatsim:" + user['cid']
        r.hmset(hash_name, user)
        r.expire(hash_name, 120)

schedule.every(60).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)