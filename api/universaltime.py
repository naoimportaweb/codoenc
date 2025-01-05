import time
import os
import ntplib

class UniversalTime:
    @staticmethod
    def now():
        try:
           
            client = ntplib.NTPClient()
            response = client.request('0.us.pool.ntp.org')
            return time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time));
        except:
            print('Could not sync with time server.');
        return None;

if __name__ == "__main__":
    print(UniversalTime.now());