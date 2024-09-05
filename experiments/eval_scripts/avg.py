import json
from functools import reduce
import numpy as np
import math
from scipy import stats

def all():
    data_sets = ["/home/gerd/thesis-workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/thesis-workspace/synthio/experiments/reproducibility_data/haswell_im.json", "/home/gerd/thesis-workspace/synthio/experiments/reproducibility_data/kabylake_im.json", "/home/gerd/thesis-workspace/synthio/experiments/reproducibility_data/broadwell_im.json"]
    for ds in data_sets:
        existing_measurements = dict()
        with open(ds, 'r+') as f:
            existing_measurements = json.load(f)

        data = dict()
        for gadget_name, gadget in existing_measurements.items():
            data[gadget_name] = dict()
            for metric_name, metric_data in gadget.items():
                is_normal = None
                conf_interval = None
                if len(metric_data) >= 8:
                    _, p_value = stats.normaltest(metric_data, nan_policy = 'omit')
                    if p_value < 0.05:
                        is_normal = False
                    else:
                        is_normal = True

                if len(metric_data) > 0:
                    if metric_name == 'l3-store-miss-rate' or metric_name == 'bad-speculation':
                        metric_data = list(np.clip(metric_data, 0.0, 1.0))
                    
                    res = stats.bootstrap((metric_data,), np.mean, confidence_level=0.9)
                    low_ci, high_ci = res.confidence_interval
                    if not math.isnan(float(low_ci)) and not math.isnan(float(high_ci)):
                        conf_interval = {"low": low_ci, "high": high_ci}
                    else:
                        conf_interval = None

                    average = (reduce(lambda x, y: x + y, metric_data)) / len(metric_data)
                    variance = np.var(metric_data)
                    cov = stats.variation(metric_data, nan_policy='omit')
                    if math.isnan(float(cov)):
                        cov = None

                    data[gadget_name][metric_name] = {"average": average, "variance": variance, "cov":cov, "normality": is_normal, "confidence_interval": conf_interval}
        dst_file = ds[:-8] + "_avg.json"
        with open(dst_file, 'w') as f:
            json.dump(data, f)

def combos():
    src_file = "/home/gerd/thesis-workspace/synthio/experiments/scrambler_c2_results/consistency_results.json"
    dst_file = "/home/gerd/thesis-workspace/synthio/experiments/combos.json"

    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
        f.seek(0)

    data = dict()
    for combo_hash, combo_data in existing_measurements.items():
        data[combo_hash] = dict()
        for key, items in combo_data.items():
            if key == 'measurements':
                new_msrm_list = list()
                for msrm in items:
                    for m, values in msrm.items():
                        average = 0.0
                        if type(values) is not list:
                            continue
                        for v in values:
                            average += v
                        average = average / len(values)
                        variance = np.var(values)
                        new_msrm_list.append({m: {'avg': average, 'var': variance}})
                        # average = (reduce(lambda x, y: x + y, values)) / len(values)
                        # new_msrm_list.append({m:average})
                data[combo_hash][key] = new_msrm_list 
                continue
            # measurements = items['measurements']
            data[combo_hash][key] = items

    with open(dst_file, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    all()
    