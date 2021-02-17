from decimal import Decimal
import os

import numpy as np


class Reporter:
    def __init__(self, abcList):
        self.abcList = abcList
        if(abcList[0].conf.PRINT_PARAMETERS):
            self.print_parameters()

        if (abcList[0].conf.RUN_INFO):
            self.run_info()
        if (abcList[0].conf.SAVE_RESULTS):
            self.save_results()
        if (abcList[0].conf.RUN_INFO_COMMANDLINE):
            self.command_line_print()


    def print_parameters(self):
        for i in range(self.abcList[0].conf.RUN_TIME):
            print(self.abcList[i].experimentID,". run")
            for j in range(self.abcList[0].conf.DIMENSION):
                print("Global Param[", j + 1, "] ", self.abcList[i].globalParams[j])

    def run_info(self):
        summ = []
        for i in range(self.abcList[0].conf.RUN_TIME):
            print(self.abcList[i].experimentID + " run: ",
                  self.abcList[i].globalOpt, " Cycle: ",
                  self.abcList[i].cycle, " Time: ",
                  self.abcList[i].globalTime)
            summ.append(self.abcList[i].globalOpt)
        print("Mean: ", np.mean(summ), " Std: ", np.std(summ), " Median: ", np.median(summ))
    def command_line_print(self):
        summ = []
        for i in range(self.abcList[0].conf.RUN_TIME):
            summ.append(self.abcList[i].globalOpt)
        print('%1.5E' % Decimal(np.mean(summ)))

    def save_results(self):
        if not os.path.exists(self.abcList[0].conf.OUTPUTS_FOLDER_NAME):
            os.makedirs(self.abcList[0].conf.OUTPUTS_FOLDER_NAME)

        header="experimentID ;Number of Population; Maximum Evaluation; Limit; Function, Dimension, Upper Bound; Lower Bound; isMinimize; Result ; Time \n"
        csvText = "{} ;{}; {}; {}; {}; {}; {}; {}; {}; {} ; {} \n"
        with open(self.abcList[0].conf.OUTPUTS_FOLDER_NAME+"/"+self.abcList[0].conf.RESULT_REPORT_FILE_NAME, 'a') as saveRes:
            if(sum(1 for _ in open(self.abcList[0].conf.OUTPUTS_FOLDER_NAME + "/" + self.abcList[0].conf.RESULT_REPORT_FILE_NAME)) < 1):
                saveRes.write(header)

            for i in range(self.abcList[0].conf.RUN_TIME):
                saveRes.write(csvText.format(
                    self.abcList[i].experimentID,
                    self.abcList[i].conf.NUMBER_OF_POPULATION,
                    self.abcList[i].conf.MAXIMUM_EVALUATION,
                    self.abcList[i].conf.LIMIT,
                    self.abcList[i].conf.OBJECTIVE_FUNCTION.__name__,
                    self.abcList[i].conf.DIMENSION,
                    self.abcList[i].conf.UPPER_BOUND,
                    self.abcList[i].conf.LOWER_BOUND,
                    self.abcList[i].conf.MINIMIZE,
                    self.abcList[i].globalOpt,
                    self.abcList[i].globalTime,

                ))

            header = "experimentID;"
            for j in range(self.abcList[0].conf.DIMENSION):

                if (j < self.abcList[0].conf.DIMENSION - 1):
                    header = header + "param" + str(j) + ";"
                else:
                    header = header + "param" + str(j) + "\n"

            with open(self.abcList[0].conf.OUTPUTS_FOLDER_NAME + "/" + self.abcList[0].conf.PARAMETER_REPORT_FILE_NAME,
                      'a') as saveRes:
                if (sum(1 for _ in open(self.abcList[0].conf.OUTPUTS_FOLDER_NAME +
                                        "/" + self.abcList[0].conf.PARAMETER_REPORT_FILE_NAME)) < 1):
                    saveRes.write(header)

                for i in range(self.abcList[0].conf.RUN_TIME):
                    csvText = str(self.abcList[i].experimentID) + ";"
                    for j in range(self.abcList[0].conf.DIMENSION):
                        if(j<self.abcList[0].conf.DIMENSION-1):
                            csvText = csvText + str(self.abcList[i].globalParams[j]) + ";"
                        else:
                            csvText = csvText + str(self.abcList[i].globalParams[j]) + "\n"
                    saveRes.write(csvText)

            for i in range(self.abcList[0].conf.RUN_TIME):
                if not os.path.exists(self.abcList[i].conf.OUTPUTS_FOLDER_NAME + "/" + self.abcList[i].conf.RESULT_BY_CYCLE_FOLDER):
                    os.makedirs(self.abcList[i].conf.OUTPUTS_FOLDER_NAME + "/" + self.abcList[i].conf.RESULT_BY_CYCLE_FOLDER)

                with open(self.abcList[i].conf.OUTPUTS_FOLDER_NAME + "/" + self.abcList[i].conf.RESULT_BY_CYCLE_FOLDER +
                          "/" + self.abcList[i].experimentID + ".txt", 'a') as saveRes:

                    for j in range(self.abcList[i].cycle):
                        saveRes.write(str(self.abcList[i].globalOpts[j]) + "\n")
