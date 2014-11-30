#!/usr/bin/env python2
# This file should control the entire application from the UI to the backend.

# Imports

import task_classes as classes
import task_scheduler as scheduler

# Control 
def main():
    print('Loading main()')
    schedules = scheduler.getUserSchedule()
    scheduler.main(schedules)

if __name__ == '__main__':
    main()
else:
    quit('This is not meant to be ran as a module.')
