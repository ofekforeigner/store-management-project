
import datetime


class logs_event():
    def __init__(self):
        pass

    def log_write_events(self):
        try:
            self.logmsg = self.msg + '\n'
            file = open("Log/log.txt", 'a+')
            file.write(self.logmsg)
            file.close()
        except:
            print('log file can not be opened')

    def query_write(self, sql_query):
        # when is a sql log call this func.
        self.msg = "SQL "
        self.msg+= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : "
        self.msg += sql_query
        self.log_write_events()

    def inf_write(self, inf):
        # when is a info log call this func.
        self.msg = "INF "
        self.msg += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : "
        self.msg += inf
        self.log_write_events()

    def err_write(self, err):
        # when is a err log call this func.
        self.msg = "ERR "
        self.msg += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : "
        self.msg = err  # save the msg.
        self.log_write_events()
