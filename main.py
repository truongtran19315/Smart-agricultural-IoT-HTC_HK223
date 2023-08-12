from RS485Controller import * 
from scheduler import *
from softwaretimer import * 

from read_sensor_task import *
from adafruit import *
from user_interface import *
import sys
import time
from images import *

###

m485  = RS485Controller()

scheduler = Scheduler()
scheduler.SCH_Init()
monitoring_timer = softwaretimer()

monitoring= MonitoringTask(m485, monitoring_timer)
main_ui = App(monitoring)

scheduler.SCH_Add_Task(main_ui.UI_Refresh, 1, 100)
scheduler.SCH_Add_Task(monitoring_timer.Timer_Run, 1, 100)
#scheduler.SCH_Add_Task(monitoring.MonitoringTask_Run, 1, 100)


while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)