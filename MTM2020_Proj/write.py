from zoautil_py import MVSCmd, Datasets
from zoautil_py.types import DDStatement
# Import datetime, needed so we can format the report
from datetime import datetime
# Import os, needed to get the environment variables
import os

class Singleton:
    __instance = None
    @staticmethod
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance
    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self
    def fun1(self, str1):
        output_dataset=os.getenv('USER')+".SOURCE.EXMP" # dataset to write the record in
        str2=str1
        if Datasets.exists(output_dataset) != True:
            print ("Dataset Created")
            Datasets.create(output_dataset, "SEQ")
            str2="Details of Customers\nDate       Time      Co  Name                   Phone        Price\n===================================\n" + str1
        
        Datasets.write(output_dataset, str2, append=True)


def fun2(str1):
    s = Singleton.getInstance()
    Singleton.fun1(s, str1)