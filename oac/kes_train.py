import datetime

from dialogs.KES_dialog.KES_calculator import KesCalculator


kes = KesCalculator()
kes.parameter_id = 'time_in'
data = '5.05.24 15:00'
print(kes.is_usable_format(data))
kes.current.value = data
kes.parameter_id = 'time_out'
data2 = '4.05.24 16:50'
kes.current.value = data2
print(kes.is_usable_format(data))
'нет обработки ошибки!'
print(kes.get_time_delta())





