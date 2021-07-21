import qasync
import asyncio
import functools
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scrape_stuff import get_google, get_bing


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

        self.initUI()

        self.schedule_jobs()

    async def start_L1(self):
        self.L1.setText('google')
        await get_google()
        self.scheduler.pause_job(job_id='1')

    async def start_L2(self):
        self.L2.setText('bing')
        await get_bing()
        self.scheduler.pause_job(job_id='2')

    def schedule_jobs(self):
        print('scheduling jobs')
        self.scheduler.add_job(self.start_L1, 'interval', seconds=1, id='1')
        self.scheduler.pause_job(job_id='1')
        self.scheduler.add_job(self.start_L2, 'interval', seconds=1, id='2')
        self.scheduler.pause_job(job_id='2')

    def start_L1_job(self):
        print('starting L1 job: google\'s homepage should have been downloaded if all went well')
        # print(self.scheduler.print_jobs())
        # print(self.scheduler.get_job('1'))
        self.scheduler.resume_job(job_id='1')

    def start_L2_job(self):
        print('starting L2 job: bing\'s homepage should have been downloaded if all went well')
        self.scheduler.resume_job(job_id='2')

    def initUI(self):
        self.L1_start_btn = QPushButton(self)
        self.L1_start_btn.setText('Download Google\'s Homepage')
        self.L1_start_btn.setGeometry(0, 0, 300, 20)
        self.L1_start_btn.clicked.connect(self.start_L1_job)

        self.L2_start_btn = QPushButton(self)
        self.L2_start_btn.setText('Download Bing\'s Homepage')
        self.L2_start_btn.setGeometry(300, 0, 300, 20)
        self.L2_start_btn.clicked.connect(self.start_L2_job)

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
