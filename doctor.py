import pandas as pd
from datetime import datetime, timedelta


def load_data():
    doctor_data = pd.read_excel('Data/doctor_data.xlsx').drop('Unnamed: 0', 1)
    return doctor_data


class Doctor:
    """
    time format = '08:00 - 08:55'
    """
    services = {'Kaisa': ['teeth check up', 'teeth removal', 'teeth whitening', 'consultation'],
                'Teemu': ['teeth check up', 'teeth removal', 'teeth whitening'],
                'Inka': ['teeth check up', 'teeth removal', 'teeth whitening', 'consultation', 'implant']}
    _available = True
    service_time = {'teeth check up': 25,
                    'teeth removal': 25,
                    'teeth whitening': 25,
                    'consultation': 20,
                    'implant': 55}
    times = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:30', '13:00', '13:30', '14:00',
             '14:30', '15:00', '15:30']

    def __init__(self, name):
        """
        :param name:
        """
        self._doctor_name = name
        self._service = self.services[self._doctor_name]
        self._available = True

    def get_reserved(self):
        return load_data().loc[load_data().Name == self._doctor_name]

    def can_provide_service(self, service):
        """
        :param service:
        :return: true or false based on whether the doctor can provide the service
        """
        if service in self._service:
            return True
        return False

    def is_available(self, date, time):
        """
        :param date:
        :param time:
        :return: self._available. true or false based on whether the doctor is available at that time
        """
        start_time = time.split('-')[0].strip()
        end_time = time.split('-')[1].strip()
        if date in self.get_reserved().Date.tolist():
            reserved = self.get_reserved().loc[self.get_reserved().Date == date]['Reserved time'].tolist()
            reserved1 = [(i.split('-')[0].strip(), i.split('-')[1].strip()) for i in reserved]
            occupied = [i for i in reserved1 if i[0] <= start_time <= i[1]] + [i for i in reserved1 if
                                                                               i[0] <= end_time <= i[1]]
            occupied = list(set(occupied))
            if len(occupied) > 0:
                self._available = False
        return self._available

    def reserve(self, date, time, service):
        if self.can_provide_service(service) and self.is_available(date, time):
            load_data().append({'Name': self._doctor_name, 'Date': date, 'Reserved time': time,
                                'Reserved service': service}, ignore_index=True).drop_duplicates().to_excel(
                'Data/doctor_data.xlsx')

    def cancel(self, date, time, service):
        df = load_data()
        df.loc[~((df['Name'] == self._doctor_name) & (df['Date'] == date) & (df['Reserved time'] == time) &
                 (df['Reserved service'] == service))].to_excel('Data/doctor_data.xlsx')

    def show_available_slots(self, date, service):
        if self.can_provide_service(service):
            if date in self.get_reserved().Date.tolist():
                reserved = set(self.get_reserved().loc[self.get_reserved().Date == date]['Reserved time'].tolist())
                reserved1 = [(i.split('-')[0].strip(), i.split('-')[1].strip()) for i in reserved]
                duration = self.service_time[service]
                reserved2 = []
                for x in reserved1:
                    reserved2.append([i for i in self.times if x[0] <= i <= x[1] or x[0] <=
                                      datetime.strftime((datetime.strptime(i, '%H:%M') + timedelta(minutes=duration)),
                                                        '%H:%M') <= x[1]])
                reserved2 = [item for sublist in reserved2 for item in sublist]
                free = set(self.times) - set(reserved2)
                free = [datetime.strptime(i, '%H:%M') for i in free]
                free.sort()
                free = [datetime.strftime(i, '%H:%M') for i in free]
                return free
            return self.times
        return []

    @property
    def service(self):
        return self._service
