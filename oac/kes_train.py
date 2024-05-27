import datetime

from dialogs.KES_dialog.KES_calculator import KesCalculator


kes = KesCalculator()

kes.parameter_id = 'time_in'
data = '5.05.24 16:50'
kes.set_value(data)
print(kes.current)

kes.parameter_id = 'time_in'
data = '4.05.24 16:50'
kes.set_value(data)
print(kes.current)

kes.parameter_id = 'time_out'
data2 = '5.05.24 17:50'
kes.set_value(data2)

rep = kes.get_answer()
print(rep)






