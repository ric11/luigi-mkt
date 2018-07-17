import luigi
from time import sleep
import time
import os
import sys
import subprocess
import datetime
import shutil
from time import strftime
from sys import executable

import csv
import sys

sys.path.insert(0, 'C:/Users/ricsor/Desktop/luigi/scripts') #enable import from other directory
sys.path.insert(0, 'C:/Users/ricsor/Desktop/luigi/scripts/utils') #enable import from other directory

#### DEFINE CURRENT DIRECTORY CLASS ####

class CurrentDirectory():
    path = os.path.dirname(os.path.abspath(__file__))



print('Running Paid Search Report Workflow...')

#### PATHS DEFINITION #######
currentDirectory = CurrentDirectory().path #INSTANTIATE THE CLASS CURRENT DIRECTORY
runRscript='C:/R/R-3.3.3/bin/Rscript'
luigiPATH='C:/Users/ricsor/Desktop/luigi'
tasksPATH='C:/Users/ricsor/Desktop/luigi/tasks'
mktintelPATH='S:/Online Marketing/Marketing Intelligence/Regulars/Hourly'
scriptPATH='C:/Users/ricsor/Desktop/luigi/scripts'
script='/wc2018_hourly_update_TEST.R'

today = time.strftime("%Y%m%d")
now = time.strftime("%Y%m%d-%H%M%S")
dayHour = time.strftime("%Y%m%d_%H")


############################# PIPELINE1 ##################################################################################



class WC2018_registrations (luigi.ExternalTask):  #TASK 1
    
    param=luigi.Parameter(default=dayHour)
    
       # return [Archive_WC2018_registrations(self.param)]
    def run(self):
        sleep(2)
        src= 'C:/Users/ricsor/Desktop/luigi/Dataset/registrations/WC2018_registrations.csv'
        subprocess.check_call([runRscript, scriptPATH+'/wc2018_hourly_update_TEST.R'], shell=False)
        file = open('C:/Users/ricsor/Desktop/luigi/archive/%s_registrationWC2018Updated.txt' %self.param,'w+') 
        file.write('Registration WC 2018 updated at %s' % self.param ) 
        file.close()
      #  dst=  'C:/Users/ricsor/Desktop/luigi/archive/keyword_final_%s.csv' % self.param    
      #  shutil.copyfile(src,dst)  
    def output(self):
        return luigi.LocalTarget('C:/Users/ricsor/Desktop/luigi/archive/%s_registrationWC2018Updated.txt' % self.param)


class Archive_WC2018_registrations (luigi.Task): #TASK 8
    param=luigi.Parameter(default=dayHour)

    def requires(self):
        return [WC2018_registrations(self.param)]

    def run(self):
        sleep(2)
        src = 'C:/Users/ricsor/Desktop/luigi/Dataset/registrations/WC2018_registrations.csv'
        dst= 'C:/Users/ricsor/Desktop/luigi/archive/%s_WC2018_registrations.csv' % self.param  
        shutil.copyfile(src,dst) 
    def output(self):
        return luigi.LocalTarget('C:/Users/ricsor/Desktop/luigi/archive/%s_WC2018_registrations.csv' % self.param)



@luigi.Task.event_handler(luigi.Event.SUCCESS)
def celebrate_success(task):
    print('We made it')


if __name__=='__main__':
   luigi.run()
    