import threading
import pymysql


def new_close(conn):
    if conn.pooling != None:
        conn.pooling.put(conn)
    elif conn.old_close != None:
        conn.old_close()

class Pool(object):
    def __init__(self, create_instance, max_count=10, timeout=10):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.in_use_list = set()
        self.free_list = set()
        self.max_count = max_count or 10
        self.timeout = timeout or 10
        self.new_instance = create_instance
        assert (create_instance != None)
        self.__change_pymysql_close()

    def __change_pymysql_close(self):
        old_close = pymysql.connections.Connection.close
        if old_close == new_close:
            return
        pymysql.connections.Connection.close = new_close
        pymysql.connections.Connection.old_close = old_close

    def get(self):
        """get one from free list"""
        with self.lock:
            if len(self.free_list) > 0:
                one = self.free_list.pop()
                self.in_use_list.add(one)
                return one
            if len(self.in_use_list) < self.max_count:
                one = self.new_instance()
                one.pooling = self
                self.free_list.add(one)
            if len(self.free_list) <= 0:
                self.condition.wait(self.timeout)
                if len(self.free_list) <= 0:
                    raise TimeoutError()
            one = self.free_list.pop()
            self.in_use_list.add(one)
            return one

    def put(self, value):
        """put one into free list"""
        with self.lock:
            self.in_use_list.remove(value)
            self.free_list.add(value)
            self.condition.notify_all()

    def size(self):
        with self.lock:
            return len(self.free_list) + len(self.in_use_list)

    def max_size(self):
        return self.max_count