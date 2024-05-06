import datetime

from dialogs.KES_dialog.KES_calculator import KesCalculator


kes = KesCalculator()
kes.parameter_id = 'time_in'
data = '5.05.24 15:00'
print(kes.is_usable_format(data))
kes.current.value = data
kes.parameter_id = 'time_out'
kes.current.value = '4.05.24 13:50'
print()
print(kes.current_params)
rep = kes.get_answer()
print(rep)



