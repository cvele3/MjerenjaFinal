import time

import nidaqmx
import nidaqmx.constants as constants
from matplotlib import pyplot

task_name = "ReadVoltageTask"
task_name2 = "REadTemperatureTask"
channel = "cDAQ9185-1F56937Mod1/ai0"
channel2 = "cDAQ9185-1F56937Mod1/ai1"
channel3 = "cDAQ9185-1F56937Mod1/ai2"

task = nidaqmx.Task(task_name)

task.ai_channels.add_ai_thrmcpl_chan(physical_channel=channel2,
                                     name_to_assign_to_channel='ThermocoupleChannel',
                                     min_val=0,
                                     max_val=100,
                                     units=constants.TemperatureUnits.DEG_C,
                                     thermocouple_type=constants.ThermocoupleType.K,
                                     cjc_source=constants.CJCSource.CONSTANT_USER_VALUE,
                                     cjc_val=25,
                                     cjc_channel='')
task.ai_channels.add_ai_resistance_chan(
    physical_channel=channel3,
    resistance_config=constants.ResistanceConfiguration.FOUR_WIRE,
    current_excit_source=constants.ExcitationSource.INTERNAL,
    current_excit_val=500.0e-6,
    units=constants.ResistanceUnits.OHMS
)

tpValues = []
pt100Values = []
dates = []
i = 1

while True:
    task.start()
    voltage = task.read()

    print("Temp couple value: ", voltage[0], "C")
    tpValues.append(voltage[0])
    print("Temp PT100 value: ", (voltage[1] - 100) / 0.33, "C")
    pt100Values.append((voltage[1] - 100) / 0.33)
    dates.append(i)
    time.sleep(0.1)

    pyplot.clf()
    pyplot.plot(dates, tpValues, label="Termopar values")
    pyplot.plot(dates, pt100Values, label="PT100 values")
    pyplot.legend()
    pyplot.pause(0.1)
    task.stop()
    i += 1

task.stop()

task.close()
