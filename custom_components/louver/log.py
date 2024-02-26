import platform
import logging
from enum import Enum

class Log:

    __instance = None

    class Level(Enum):
        E = 0
        W = 1
        I = 2
        D = 3

    def __init__(self):
        self.__name = "louver"
        self.__logger = None
        Log.__instance = None

    @staticmethod
    def configure(name : str):
        if (Log.__instance == None):
            Log.__instance = Log()
        Log.__instance.__name = name
        Log.__instance.__logger = logging.getLogger(name)

    @staticmethod
    def error(module : str, message : str):
        Log.formatedOut(Log.Level.E, module, message)

    @staticmethod
    def warning(module : str, message : str):
        Log.formatedOut(Log.Level.W, module, message)

    @staticmethod
    def info(module : str, message : str):
        Log.formatedOut(Log.Level.I, module, message)

    @staticmethod
    def debug(module : str, message : str):
        Log.formatedOut(Log.Level.D, module, message)
        
    @staticmethod
    def formatedOut(level : Level, module : str, message : str):
        levelStr = ""
        if (level == Log.Level.E):
            levelStr = "E"
        elif (level == Log.Level.W):
            levelStr = "W"
        elif (level == Log.Level.I):
            levelStr = "I"
        elif (level == Log.Level.D):
            levelStr = "D"
        s = "{}: {}: {}".format(levelStr, module, message)
        if (Log.__instance is not None):
            if (level == Log.Level.E):
                Log.__instance.__logger.error(s)
            elif (level == Log.Level.W):
                Log.__instance.__logger.warning(s)
            elif (level == Log.Level.I):
                Log.__instance.__logger.info(s)
            elif (level == Log.Level.D):
                Log.__instance.__logger.debug(s)
        #print(s)
