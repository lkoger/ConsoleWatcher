from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
from datetime import datetime
from time import sleep

from sqlalchemy import false

def exception_info(exception):
    print('Exception:')
    print(type(exception))
    print(exception.args)
    print(exception)

class ConsoleWatcher:
    def __init__(self, urls, config) -> None:
        self.urls = urls
        self.availability = {}

        # Get any config data
        #config = json.load(open('config.json'))
        self.webhook = config['discord_webhook']
        self.repeat_delay = config['repeat_delay_minutes']
        self.availability_recheck_delay = config["availability_recheck_delay_minutes"]

        # Set up selenium driver
        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(options=opts)

    def found(self, key):
        msg = f'Found {key}: {self.urls[key]}'
        data = {'content': msg}
        print(f'Sending "{msg}" to discord... ', end='')
        requests.post(self.webhook, data=data)
        print('Sent.')
        self.availability[key] = datetime.now()
    
    def should_check(self, key):
        if key in self.availability:
            delta = (datetime.now() - self.availability[key]).total_seconds()
            if delta < (self.availability_recheck_delay * 60):
                return False
        
        return True

    def time_to_resume(self):
        # If these lens aren't the same, we know that at least one
        # url hasn't been determined to be available. In which case,
        # assume that we'll wait at least for the repeat_delay time.
        if len(self.urls) > len(self.availability):
            return self.repeat_delay * 60
        else:
            # Need to get all the time differences between when they
            # were found to be available, and now.
            deltas = []
            for key in self.availability:
                deltas.append(datetime.now() - self.availability[key])

            # Compare max time difference to the availability_recheck_delay
            max_delta = max(deltas)
            resume_time_seconds = (self.availability_recheck_delay*60) - max_delta.total_seconds()
            # Time could be negative if max_delta is greater than the availability_recheck_delay
            # If so, just return the repeat_delay time
            if resume_time_seconds > 0:
                # If time is greater than 0, return max(resume_time, self.repeat_delay) * 60
                # Reason being that we always want to wait at least repeat_delay.
                # But if all checked urls are listed as available, we don't want to
                # ever check again before availability_recheck_delay elapses. And this
                # value should be significantly more than repeat_delay to avoid spamming.
                return max(resume_time_seconds, self.repeat_delay * 60)
            else:
                return self.repeat_delay * 60

    def check_availability(self):
        while True:
            for key in self.urls:
                if self.should_check(key):
                    try:
                        self.driver.get(self.urls[key])
                        try:
                            elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-test='orderPickupMessage']")))
                            if elem:
                                self.found(key)
                        except TimeoutException:
                            #print(f'{key} at {self.urls[key]} is unavailable')
                            continue
                        except Exception as e:
                            exception_info(e)
                    except Exception as e:
                        exception_info(e)
            
            now = datetime.now()
            resume_time = self.time_to_resume()
            print(f'Sleeping for {resume_time} seconds...')
            sleep(resume_time)
            print('Resuming...')
