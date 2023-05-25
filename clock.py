from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=3)
def timed_job():
    print('Run spiders every 3 hours.')
    subprocess.run(["python", "run_spider.py"])

sched.start()
