from scipy import stats
import json
from functools import reduce
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
import imgkit
import dataframe_image as dfi
import plotly.figure_factory as ff

def test_normality():
    src_file = "/home/gerd/Workspace/synthio/experiments/reproducibility_data/zen3_im.json"
    dst_file = "/home/gerd/Workspace/synthio/experiments/reproducibility_data/zen3_avg.json"
    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
        # f.seek(0)

    data = dict()
    for gadget_name, gadget in existing_measurements.items():
        data[gadget_name] = dict()
        for metric_name, metric_data in gadget.items():
            is_normal = None
            conf_interval = None
            if len(metric_data) >= 8:
                _, p_value = stats.shapiro(metric_data)

                if math.isnan(float(p_value)):
                    p_value = None
                else:
                    if p_value < 0.05:
                        is_normal = False
                    else:
                        is_normal = True

            if len(metric_data) > 0:
                res = stats.bootstrap((metric_data,), np.mean, confidence_level=0.9)
                low_ci, high_ci = res.confidence_interval
                if not math.isnan(float(low_ci)) and not math.isnan(float(high_ci)):
                    conf_interval = {"low": low_ci, "high": high_ci}
                else:
                    conf_interval = None
            else:
                continue
            average = (reduce(lambda x, y: x + y, metric_data)) / len(metric_data)
            variance = np.var(metric_data)
            std = np.std(metric_data)
            cov = stats.variation(metric_data, nan_policy='omit')
            if math.isnan(float(cov)):
                cov = None

            data[gadget_name][metric_name] = {"average": average, "variance": variance, "std":std, "cov":cov, "normality": is_normal, "nml_score": p_value, "confidence_interval": conf_interval}

    with open(dst_file, 'w') as f:
        json.dump(data, f)

def kruskal_wallis():
    data_sets = ["/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/kabylake_im.json"]
    # data_sets = ["/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/haswell_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/kabylake_im.json"]
    data_frames = list()

    for ds in data_sets:
        with open(ds, 'r+') as f:
            existing_measurements = json.load(f)
            data_frames.append(existing_measurements)

    kruskal_set = dict()

    #group metrics for all data-sets
    for gadget_name, gadget_data in data_frames[0].items():
        kruskal_set[gadget_name] = dict()
        for metric_name, metric_data in gadget_data.items():
            if len(metric_data) == 0:
                continue
            kruskal_set[gadget_name][metric_name] = [metric_data]
            for other in data_frames[1:]:
                if len(other[gadget_name][metric_name]) == 0:
                    continue
                kruskal_set[gadget_name][metric_name].append(other[gadget_name][metric_name])
    
    results = dict()
    for gadget, metrics in kruskal_set.items():
        results[gadget] = dict()
        if len(metrics) <= 1:
            continue

        for n, x in metrics.items():
            if "rate" not in n and "boundedness" not in n and "cpi" not in n and "page" not in n:
                continue

            if len(x) <=1:
                results[gadget][n] = -1
                continue

            iii = list()
            for i in x:
                if len(i) > 10:
                    iii.append(i[:10])
            
            # print(iii)
            try:
                res = stats.kruskal(*iii)
            except:
                results[gadget][n] = -1
                continue

            if not math.isnan(float(res.pvalue)) and not math.isnan(float(res.pvalue)):
                accept = None
                if res.pvalue < 0.01:
                    accept = False
                else:
                    accept = True
                results[gadget][n] = {"p_value": res.pvalue, "accept": accept}
            else:
                results[gadget][n] = -1

            # previous_p = res.pvalue
            # if accept is False:
            #     res = stats.f_oneway(*iii)
            #     if not math.isnan(float(res.pvalue)) and not math.isnan(float(res.pvalue)):
            #         accept = False
            #     if res.pvalue < 0.01:
            #         accept = False
            #         results[gadget][n] = {"p_value": previous_p, "accept": accept}
            #     else:
            #         accept = True
            #         results[gadget][n] = {"p_value": res.pvalue, "accept": accept}

    # print(results)
    
    with open('/home/gerd/Workspace/synthio/experiments/reproducibility_data/kw_results.json', 'w') as f:
        json.dump(results, f)
 
def wilcoxon_pairwise():
    pair_one = ["/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/kabylake_im.json"]
    # data_sets = ["/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/kabylake_im.json"]
    data_frames = list()

    for ds in pair_one:
        with open(ds, 'r+') as f:
            existing_measurements = json.load(f)
            data_frames.append(existing_measurements)

    wily_set = dict()

    #group metrics for all data-sets
    for gadget_name, gadget_data in data_frames[0].items():
        wily_set[gadget_name] = dict()
        for metric_name, metric_data in gadget_data.items():
            if len(metric_data) == 0:
                continue
            wily_set[gadget_name][metric_name] = [metric_data]
            for other in data_frames[1:]:
                if len(other[gadget_name][metric_name]) == 0:
                    continue
                wily_set[gadget_name][metric_name].append(other[gadget_name][metric_name])
    
    results = dict()
    for gadget, metrics in wily_set.items():
        results[gadget] = dict()
        if len(metrics) <= 1:
            continue

        for n, x in metrics.items():
            if len(x) <=1:
                results[gadget][n] = -1
                continue
            res = stats.wilcoxon(*x)
            if not math.isnan(float(res.pvalue)) and not math.isnan(float(res.pvalue)):
                results[gadget][n] = res.pvalue
            else:
                results[gadget][n] = -1

    # print(results)
    
    with open('/home/gerd/Workspace/synthio/experiments/reproducibility_data/wilcoxon_results.json', 'w') as f:
        json.dump(results, f)
def violin():
    gadgets_metrics_to_draw = {"bp_gadget_c1": ["br-miss-rate"], "cache_gadget_c13": ["l3-store-miss-rate"],  "cache_gadget_c8": ["l3-store-miss-rate"], "cache_gadget_c1": ["l1-load-miss-rate"], "bp_gadget_c6": ['cpi'], }

    data_sets = ["/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/haswell_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/kabylake_im.json", "/home/gerd/Workspace/synthio/experiments/reproducibility_data/broadwell_im.json"]
    data_frames = list()
    environments = ["skylake", "haswell", "kabylake", "broadwell"]
    for i, ds in enumerate(data_sets):
        with open(ds, 'r+') as f:
            existing_measurements = json.load(f)
            existing_measurements['environment'] = environments[i]
            data_frames.append(existing_measurements)

    violin_sets = dict()

    #group metrics for all data-sets
    for frame in data_frames:
        env = frame['environment']
        for gadget_name, gadget_data in frame.items():
            if gadget_name not in gadgets_metrics_to_draw:
                continue
        
            if gadget_name not in violin_sets:
                violin_sets[gadget_name] = dict()
    
            for metric_name, metric_data in gadget_data.items():
                if metric_name not in gadgets_metrics_to_draw[gadget_name]:
                    continue
                if metric_name not in violin_sets[gadget_name]:
                    violin_sets[gadget_name][metric_name] = dict()

                if len(metric_data) == 0:
                    continue

                if metric_name == 'l3-store-miss-rate' or metric_name == 'bad-speculation':
                    metric_data = list(np.clip(metric_data, 0.0, 1.0))

                violin_sets[gadget_name][metric_name][env] = metric_data
    with open('/home/gerd/Workspace/synthio/experiments/reproducibility_data/violin.json', 'w') as f:
        json.dump(violin_sets, f)

def flatten_dict(nested_dict):
    res = {}
    if isinstance(nested_dict, dict):
        for k in nested_dict:
            flattened_dict = flatten_dict(nested_dict[k])
            for key, val in flattened_dict.items():
                key = list(key)
                key.insert(0, k)
                res[tuple(key)] = val
    else:
        res[()] = nested_dict
    return res


def nested_dict_to_df(values_dict):
    flat_dict = flatten_dict(values_dict)
    df = pd.DataFrame.from_dict(flat_dict, orient="index")
    df.index = pd.MultiIndex.from_tuples(df.index)
    df = df.unstack(level=-1)
    df.columns = df.columns.map("{0[1]}".format)
    return df

def pandas():
    files = ["kabylake_avg.json", "haswell_avg.json", "broadwell_avg.json"]
    for f in files: 
        with open("/home/gerd/Workspace/synthio/experiments/reproducibility_data/" + f, 'r+') as d:
            existing_measurements = json.load(d)
            # f.seek(0)

        df = pd.DataFrame({"strings": ["Adam", "Mike"],
        "ints": [1, 3],
        "floats": [1.123, 1000.23]
        })

        frame_cg = dict()
        frame_bp = dict()
        for gadget_name, gadget in existing_measurements.items():
            if "cache" in gadget_name:
                frame_cg[gadget_name] = dict()
                for metric_name, metric_data in gadget.items():
                    if "cpi" not in metric_name and "rate" not in metric_name and "page" not in metric_name:
                        continue
                    if metric_data['cov'] is None:
                        frame_cg[gadget_name][metric_name] = -1
                        continue
                    frame_cg[gadget_name][metric_name] = round(metric_data['cov'], 6)
            else:
                frame_bp[gadget_name] = dict()
                for metric_name, metric_data in gadget.items():
                    if "cpi" not in metric_name and "rate" not in metric_name and "speculation" not in metric_name and "boundedness" not in metric_name:
                        continue    
                    if metric_data['cov'] is None:
                        frame_cg[gadget_name][metric_name] = -1
                        continue

                    frame_bp[gadget_name][metric_name] = round(metric_data['cov'], 6)

        df = nested_dict_to_df(frame_cg)
        df.to_excel(f[:8] + "_cg_cov.xlsx")
        df = nested_dict_to_df(frame_bp)
        df.to_excel(f[:8]+ "_bpg_cov.xlsx")

if __name__ == "__main__":
    violin()