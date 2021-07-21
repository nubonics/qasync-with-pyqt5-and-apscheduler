import qasync
import asyncio
import functools
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
# from apscheduler.schedulers.qt import QtScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def gen1():
    counter = 0
    while True:
        counter += 1
        yield str(counter)


def gen2():
    counter = 0
    while True:
        counter += 1
        yield str(counter)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.G1 = gen1()
        self.G2 = gen2()

        # self.scheduler = QtScheduler()
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

        self.initUI()

        self.schedule_jobs()

    def start_L1(self):
        self.L1.setText(next(self.G1))

    def start_L2(self):
        self.L2.setText(next(self.G2))

    def schedule_jobs(self):
        print('scheduling jobs')
        self.scheduler.add_job(self.start_L1, 'interval', seconds=1, id='1')
        self.scheduler.pause_job(job_id='1')
        self.scheduler.add_job(self.start_L2, 'interval', seconds=1, id='2')
        self.scheduler.pause_job(job_id='2')

    def start_L1_job(self):
        print('starting L1 job: this schedule doesnt do anything gui related atm')
        # print(self.scheduler.print_jobs())
        # print(self.scheduler.get_job('1'))
        self.scheduler.resume_job(job_id='1')

    def stop_L1_job(self):
        print('stopping L1 job')
        self.scheduler.pause_job(job_id='1')

    def start_L2_job(self):
        print('starting L2 job: the L2 label in the gui should now be updated every second')
        self.scheduler.resume_job(job_id='2')

    def stop_L2_job(self):
        print('stopping L2 job')
        self.scheduler.pause_job(job_id='2')

    def initUI(self):
        self.L1_start_btn = QPushButton(self)
        self.L1_start_btn.setText('Start L1')
        self.L1_start_btn.setGeometry(0, 0, 100, 20)
        self.L1_start_btn.clicked.connect(self.start_L1_job)
        self.L1_stop_btn = QPushButton(self)
        self.L1_stop_btn.setText('Stop L1')
        self.L1_stop_btn.setGeometry(0, 30, 100, 20)
        self.L1_stop_btn.clicked.connect(self.stop_L1_job)

        self.L2_start_btn = QPushButton(self)
        self.L2_start_btn.setText('Start L2')
        self.L2_start_btn.setGeometry(100, 0, 100, 20)
        self.L2_start_btn.clicked.connect(self.start_L2_job)
        self.L2_stop_btn = QPushButton(self)
        self.L2_stop_btn.setText('Stop L2')
        self.L2_stop_btn.setGeometry(100, 30, 100, 20)
        self.L2_stop_btn.clicked.connect(self.stop_L2_job)

        self.setGeometry(750, 300, 500, 350)
        self.setWindowTitle('PyQt5 & AsyncIOScheduler')

        self.L1 = QLabel(self)
        self.L1.setGeometry(250, 100, 100, 20)
        self.L1.setText('L1')
        self.L2 = QLabel(self)
        self.L2.setGeometry(250, 150, 100, 20)
        self.L2.setText('L2')

        self.show()


async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel("Close Application")

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, 'aboutToQuit'):
        getattr(app, 'aboutToQuit')\
            .connect(functools.partial(close_future, future, loop))

    mainWindow = MainWindow()
    mainWindow.show()

    await future

    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
