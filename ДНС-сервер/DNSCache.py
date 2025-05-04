import pickle
import os
from collections import defaultdict
from time import time
from threading import Timer


class DNSCache:
    def __init__(self, cleanup_interval=600):
        self.CACHE_FILE = "dns_cache.pkl"
        self.cache = defaultdict(dict)
        self.cleanup_interval = cleanup_interval
        self._load_cache()
        self._start_cleanup_timer()

    def _start_cleanup_timer(self):
        self.cleanup_timer = Timer(self.cleanup_interval, self._periodic_cleanup)
        self.cleanup_timer.daemon = True
        self.cleanup_timer.start()

    def _periodic_cleanup(self):
        self.clear_expired()
        self._start_cleanup_timer()

    def get(self, qname, qtype):
        try:
            if qtype not in self.cache or qname not in self.cache[qtype]:
                return None
            expire_time, records = self.cache[qtype][qname]
            if time() > expire_time:
                self.cache[qtype].pop(qname, None)
                return None
            return records
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    def put(self, qname, qtype, records, ttl):
        try:
            if not records:
                return
            expire_time = time() + ttl
            self.cache[qtype][qname] = (expire_time, records)
        except Exception as e:
            print(f"Cache put error: {e}")

    def clear_expired(self):
        try:
            current_time = time()
            for qtype in list(self.cache.keys()):
                self.cache[qtype] = {
                    qname: data for qname, data in self.cache[qtype].items()
                    if current_time <= data[0]
                }
        except Exception as e:
            print(f"Cache cleanup error: {e}")

    def save_cache(self):
        try:
            with open(self.CACHE_FILE, 'wb') as f:
                self.clear_expired()
                pickle.dump(dict(self.cache), f)
                print("Cache was saved")
        except Exception as e:
            print(f"Cache save error: {e}")

    def _load_cache(self):
        try:
            if os.path.exists(self.CACHE_FILE):
                with open(self.CACHE_FILE, 'rb') as f:
                    loaded_cache = pickle.load(f)
                    current_time = time()
                    for qtype, records in loaded_cache.items():
                        self.cache[qtype] = {
                            qname: data for qname, data in records.items()
                            if current_time <= data[0]
                        }
                print("Cache was loaded")
            else:
                print("Cache is empty")
        except Exception as e:
            print(f"Cache load error: {e}")

    def __del__(self):
        self.save_cache()
        if hasattr(self, 'cleanup_timer'):
            self.cleanup_timer.cancel()