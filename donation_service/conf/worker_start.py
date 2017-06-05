from rq import Connection, Worker

with Connection():
        qs = ['new_lmd']
        # TODO check why the exception handling is not working
        w = Worker(qs)
        w.work()
