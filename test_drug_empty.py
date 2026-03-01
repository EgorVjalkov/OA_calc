from oac.program_logic.patient import Patient

p = Patient()
p.func_id = 'drug_count'
p.set_current_params()
p.params.data['weight'].value = "70"
p.change_func()
try:
    res = p.get_result()
    print("Result:")
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
