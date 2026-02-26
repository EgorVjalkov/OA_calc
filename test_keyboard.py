from oac.program_logic.patient import Patient
import traceback

print("Testing keyboard input...")
try:
    p = Patient()
    p.func_id = 'apacheII_count'
    p.set_current_params()
    
    # Simulate keyboard input (Telegram gives strings)
    param = p.params.data['age']
    print(f"Original age: {param.value}")
    param.value = "50"
    print(f"New age: {param.value}")
    
    param = p.params.data['body_temp']
    param.value = "36.6"
    print(f"New temp: {param.value}")

    print("Success!")
except Exception as e:
    print("FAILED!")
    traceback.print_exc()
