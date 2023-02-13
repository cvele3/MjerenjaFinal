import nidaqmx
import time
import nidaqmx.constants as constants
import nidaqmx.system as system
from matplotlib import pyplot
from datetime import datetime
from random import randrange
from matplotlib.animation import FuncAnimation

# Define the task name and channel to read from
task_name = "ReadVoltageTask"
task_name2 = "REadTemperatureTask"
channel = "cDAQ9185-1F56937Mod1/ai0"
channel2 = "cDAQ9185-1F56937Mod1/ai1"
channel3 = "cDAQ9185-1F56937Mod1/ai2"

task = nidaqmx.Task(task_name)
# task2 = nidaqmx.Task(task_name2)


x_data, y_data = [], []

figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')


# def update(frame):
#     print("heok", frame)
#     x_data.append(datetime.now())
#     y_data.append(frame)
#     line.set_data(x_data, y_data)
#     figure.gca().relim()
#     figure.gca().autoscale_view()
#     return line,
#
#
# animation = FuncAnimation(figure, update, interval=1000)
# pyplot.show()



# task.ai_channels.add_ai_voltage_chan(physical_channel=channel,
#                                     name_to_assign_to_channel='VoltageChannel',
#                                     terminal_config=constants.TerminalConfiguration.DIFF,
#                                     min_val=-0.125,
#                                     max_val=0.125,
#                                     units=constants.VoltageUnits.VOLTS)
#
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


# define function that converts resistance to temperature
def resistance_to_temperature(resistance):
    a = 3.9083e-3
    b = -5.775e-7
    c = -4.183e-12
    r0 = 1000
    temperature = (-a + (a ** 2 - 4 * b * (c - (resistance / r0))) ** 0.5) / (2 * b)
    return temperature


tpValues = []
pt100Values = []
dates = []

i = 1


while True:
    task.start()
    # task2.start()

    voltage = task.read()
    # print(len(voltage))

    # print("Voltage value: ", voltage[0], "mV")
    print("Temp couple value: ", voltage[0], "C")
    tpValues.append(voltage[0])
    # print("Resistance value: ", voltage[1], "Ohms")
    print("Temp PT100 value: ", (voltage[1] - 100) / 0.33, "C")
    # print("Resistance value: ", voltage[1], "Ohms")
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

    # task2.stop()


# plot lines


task.stop()
# task2.stop()

task.close()
# task2.close()
