from doctor import Doctor
import pandas as pd
from datetime import datetime, timedelta


def load_data():
    customer_data = pd.read_excel('Data/customer_data.xlsx').drop('Unnamed: 0', 1)
    return customer_data.drop_duplicates()


def cancel_df():
    cancel_df = pd.read_excel('Data/late_cancellation.xlsx').drop('Unnamed: 0', 1)
    return cancel_df.drop_duplicates()


class Customer:

    def __init__(self, name, phone, email=None):
        self._name = name.lower()
        self._phone = phone
        self._email = email
        self._faulty_cancellation = False

    def is_customer(self):
        if self._phone in load_data().Phone.tolist():
            return True
        return False

    @staticmethod
    def date_time_combine(date, time):
        return datetime.strptime(date + ' ' + time.split('-')[0].strip(), '%Y-%m-%d %H:%M')

    @staticmethod
    def get_future_events(name, phone):
        try:
            df = load_data().loc[(load_data().Name == name.lower()) & (load_data().Phone == phone)]
            df['start_time'] = df.apply(lambda x: Customer.date_time_combine(x['Reserved date'], x['Reserved time']),
                                        axis=1)
            if df.shape[0] > 0:
                if df.loc[df['start_time'] >= datetime.today()].shape[0] > 0:
                    return df.loc[df['start_time'] >= datetime.today()]
            return None
        except:
            return None

    @classmethod
    def get_booked(cls, name, phone):
        try:
            if load_data().loc[(load_data().Name == name.lower()) & (load_data().Phone == phone)].shape[0] > 0:
                return load_data().loc[(load_data().Name == name) & (load_data().Phone == phone)]
            else:
                print('record not found')
                return None
        except:
            print('No record found')
            return None

    def reserve(self, date, time, service, doctor):
        if service in Doctor(doctor).service and Doctor(doctor).is_available(date, time):
            start_time = time.split('-')[0].strip()
            end_time = time.split('-')[1].strip()
            df = self.get_booked(self._name, self._phone)
            if df is not None:
                if date in df['Reserved date'].tolist():
                    reserved = df.loc[df['Reserved date'] == date]['Reserved time'].tolist()
                    reserved1 = [(i.split('-')[0].strip(), i.split('-')[1].strip()) for i in reserved]
                    occupied = [i for i in reserved1 if i[0] <= start_time <= i[1]] + [i for i in reserved1 if
                                                                                       i[0] <= end_time <= i[1]]
                    occupied = list(set(occupied))
                    if len(occupied) > 0:
                        return 'You have booked the same time with another doctor!'

            Doctor(doctor).reserve(date, time, service)
            load_data().append({'Name': self._name, 'Phone': self._phone, 'Email': self._email,
                                'Reserved date': date, 'Reserved time': time, 'Reserved service': service,
                                'Reserved doctor': doctor}, ignore_index=True).drop_duplicates().to_excel(
                'Data/customer_data.xlsx')

    def cancel(self, date, time, service, doctor):
        df = load_data()
        tim = self.date_time_combine(date, time)
        if datetime.now() + timedelta(days=1) <= tim:
            val = 'Cancellation handled, thank you!'
        else:
            self._faulty_cancellation = True
            val = 'Cancellation confirmed. You will be\nchanged 40€ for late cancellation!'
            cancel_df().append(
                {'date': date, 'time': time, 'service': service, 'doctor': doctor, 'customer': self._name,
                 'phone': self._phone, 'late cancellation': '40€'}, ignore_index=True).drop_duplicates().to_excel(
                'Data/late_cancellation.xlsx')
        Doctor(doctor).cancel(date, time, service)
        df.loc[~((df['Name'] == self._name) & (df.Phone == self._phone) & (
                df['Reserved date'] == date) & (df['Reserved time'] == time) &
                 (df['Reserved service'] == service) & (df['Reserved doctor'] == doctor))].drop_duplicates(). \
            to_excel('Data/customer_data.xlsx')
        return val
