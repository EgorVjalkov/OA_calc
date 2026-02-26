from oac.program_logic.patient import Patient
import traceback

dummy_data = {
    "height": 170,
    "weight": 70,
    "weight_before": 65,
    "bleed_vol": 500,
    "fetus": "normal_f",
    "bladder": "normal_b",
    "discomfort": "no_discomfort",
    "time_in": "20.10.20 10:00",
    "time_out": "20.10.20 12:00",
    "fio2": 0.4,
    "pao2": 100,
    "resp_support": "normal_resp",
    "plt": 250,
    "bili": 15,
    "hypotension": "normal_hd",
    "glasgow": 15,
    "crea": 80,
    "diuresis": 1500,
    "age": 45,
    "body_temp": 36.6,
    "mean_pressure": 80,
    "heart_rate": 75,
    "breath_rate": 16,
    "paco2": 40,
    "pH": 7.4,
    "Na": 140,
    "K": 4.5,
    "Hct": 0.4,
    "WBC": 6.5,
    "chronic": "no_chronic",
    "operation": "no_oper"
}

funcs = [
    'blood_vol_count', 
    'bleed_%_count', 
    'drag_count', 
    'sma_count', 
    'sofa_count', 
    'apacheII_count', 
    'apacheIIFio2less50_count'
]

for func_id in funcs:
    print(f"\n--- Testing {func_id} ---")
    try:
        p = Patient()
        p.func_id = func_id
        
        p.set_current_params()
        
        # Populate matching parameters
        for param_id in p.params.current_params:
            if param_id in dummy_data:
                p.params.data[param_id].value = dummy_data[param_id]
            else:
                print(f"Warning: dummy data missing for {param_id}")
                
        p.change_func()
        result = p.get_result()
        print("SUCCESS! Output length:", len(str(result)))
    except Exception as e:
        print("FAILED!")
        traceback.print_exc()

