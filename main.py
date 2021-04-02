from customer import load_data
from datetime import datetime, timedelta
# need scheduler service to run every minutes


def reminder():
    data = load_data()
    data['tim'] = data.apply(
        lambda x: datetime.strptime(x['Reserved date'] + ' ' + x['Reserved time'].split('-')[0].strip(),
                                    '%Y-%m-%d %H:%M'), axis=1)
    for i in data['tim']:
        if datetime.now() + timedelta(minutes=60) == i:
            print('Please remember your booking!')


if __name__ == '__main__':
    reminder()

