import datetime

from dialogs.KES_dialog.KES_calculator import KesCalculator, TimeError


kes = KesCalculator()

kes.parameter_id = 'time_in'
data = '5.05.24 16:50'
kes.set_value(data)
print(kes.current)

kes.parameter_id = 'time_out'
data2 = '4.05.24 16:50'
kes.set_value(data2)
print(kes.current)






