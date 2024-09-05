from scipy import stats
import json
from functools import reduce
import numpy as np
import math
import matplotlib.pyplot as plt
import base64

def big_exp():
    src_file = "/home/gerd/Workspace/synthio/experiments/consistency_data/combos.json"
    dst_file = "/home/gerd/Workspace/synthio/experiments/consistency_data/avg_combos.json"

    im_avg_file = "/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_avg.json"
    im_file = "/home/gerd/Workspace/synthio/experiments/reproducibility_data/skylake_im.json"


    counters_mapping = {
        'bp_gadget_c1': ['br-miss-rate', 'br-conditionals-miss-rate'],
        'bp_gadget_c2': ['br-miss-rate'],
        'bp_gadget_c4': ['br-miss-rate', 'br-conditionals-miss-rate'],
        'bp_gadget_c5': ['br-miss-rate'],
        'bp_gadget_c6': ['br-miss-rate', 'br-conditionals-miss-rate'],
        'bp_gadget_c7': ['br-miss-rate', 'br-conditionals-miss-rate'],
        'bp_gadget_c8': ['br-miss-rate', 'br-conditionals-miss-rate'],
        'cache_gadget_c1': ['l1-load-miss-rate', 'l2-load-miss-rate'],
        'cache_gadget_c2': ['l1-load-miss-rate', 'l2-load-miss-rate', 'l3-load-miss-rate'],
        'cache_gadget_c3': ['l1-load-miss-rate', 'l2-load-miss-rate'],
        'cache_gadget_c4': ['l1-load-miss-rate', 'l2-load-miss-rate'],
        'cache_gadget_c5': ['l1-load-miss-rate', 'l2-load-miss-rate', 'l3-load-miss-rate'],
        'cache_gadget_c6': ['l1-load-miss-rate', 'l2-load-miss-rate', 'l3-load-miss-rate'],
        'cache_gadget_c7': ['l1-load-miss-rate', 'l3-store-miss-rate'],
        'cache_gadget_c8': ['l3-store-miss-rate'],
        'cache_gadget_c13': ['l3-load-miss-rate', 'l3-store-miss-rate']
    }

    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
        # f.seek(0)

    data = dict()
    for hashed_id, report in existing_measurements.items():
        variants = report['variants']
        data[hashed_id] = {'variants': variants, 'measurements': {}}

        var_one = variants[0][2:]
        var_two = variants[1][2:]

        applicable_metrics = [x for x in counters_mapping[var_one] if x in counters_mapping[var_two]]

        for metric_name, metric_data in report['measurements'][0].items():

            if metric_name not in applicable_metrics:
                continue

            is_normal = None
            conf_interval = None


            if len(metric_data) >= 8:
                _, p_value = stats.shapiro(metric_data)
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

            average = (reduce(lambda x, y: x + y, metric_data)) / len(metric_data)
            variance = np.var(metric_data)
            cov = stats.variation(metric_data, nan_policy='omit')
            if math.isnan(float(cov)):
                cov = None

            expected_mean = None

            im_data = dict()
            with open(im_avg_file, 'r+') as f:
                im_data = json.load(f)
            
            var_one_refs = None
            var_one_rates = None
            var_two_refs = None
            var_two_rates = None
            var_one_misses = None
            var_two_misses = None

            if metric_name == "br-miss-rate":
                var_one_refs = im_data[var_one]['branch-references']['average']
                var_two_refs = im_data[var_two]['branch-references']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            elif metric_name == "br-conditionals-miss-rate":
                var_one_refs = im_data[var_one]['branch-conditional-references']['average']
                var_two_refs = im_data[var_two]['branch-conditional-references']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            elif metric_name == "l1-load-miss-rate":
                var_one_refs = im_data[var_one]['l1-loads']['average']
                var_two_refs = im_data[var_two]['l1-loads']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            elif metric_name == "l2-load-miss-rate":
                var_one_refs = im_data[var_one]['l2-loads']['average']
                var_two_refs = im_data[var_two]['l2-loads']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            elif metric_name == "l3-load-miss-rate":
                var_one_refs = im_data[var_one]['l3-loads']['average']
                var_two_refs = im_data[var_two]['l3-loads']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            elif metric_name == "l3-store-miss-rate":
                var_one_refs = im_data[var_one]['l3-stores']['average']
                var_two_refs = im_data[var_two]['l3-stores']['average']
                var_one_rates = im_data[var_one][metric_name]['average']
                var_two_rates = im_data[var_two][metric_name]['average']
            else:
                pass
            
            if var_one_refs is not None or var_two_refs is not None:
                var_one_misses = var_one_rates * var_one_refs
                var_two_misses = var_two_rates * var_two_refs
                expected_mean = (var_one_misses + var_two_misses) / (var_one_refs + var_two_refs)

            #TODO if normality is given, perform "one-sample t-test"
            #else report difference

            ts_result = 0.0
            ts_accept = None
            accept = None
            p_value = 0.0
            diff = 0.0
            # if var_one == var_two:
            #     with open(im_file, 'r+') as f:
            #         im_data = json.load(f)

            #     original = im_data[var_one][metric_name]
                
            #     ts_result = 0.0

            #     p_one = stats.kruskal(original, metric_data).pvalue
            #     p_two = stats.f_oneway(original, metric_data).pvalue

            #     if p_two > p_one and p_two >= 0.05:
            #         ts_result = p_two
            #     else: 
            #         ts_result = p_one

            #     ts_accept = False
            #     if ts_result < 0.05:
            #         ts_accept = False
            #     else:
            #         ts_accept = True
            # else:
            if expected_mean is not None:

                if is_normal:
                    p_value = stats.ttest_1samp(metric_data[:10], expected_mean, alternative='less').pvalue
                    if p_value < 0.01: #! in favor of the NULL
                        accept = False
                    else:
                        accept = True

            if expected_mean is not None:
                diff = expected_mean - np.mean(metric_data)

            data[hashed_id]['measurements'][metric_name] = {"original_sample": metric_data, "mean_diff": diff, "accept": accept, "p_value":p_value, "expected_avg": expected_mean, "average": average, "variance": variance, "cov":cov, "normality": is_normal, "confidence_interval": conf_interval}

    with open(dst_file, 'w') as f:
        json.dump(data, f)


def report_ordering_contradictions():
    src_file = "/home/gerd/Workspace/synthio/experiments/consistency_data/avg_combos.json"

    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
    
    bd = dict()

    for hashed_id, report in existing_measurements.items():
        variants = report['variants']
        var_one = variants[0][2:]
        var_two = variants[1][2:]

        if var_one == var_two:
            continue

        #TODO invert the hash
        hashed_variants = "1_"+ var_two +";2_" + var_two
        inverted_hash = (base64.b64encode(hashed_variants.encode('ascii'))).decode('utf-8')

        other_report = existing_measurements[inverted_hash]
        for metric_name, metric_data in report['measurements'].items():
            verdict = metric_data['accept']
            other_verdict = other_report['measurements'][metric_name]['accept']
            if (verdict is True and other_verdict is False) or (verdict is False and other_verdict is True):
                
                accept = None
                other_data = other_report['measurements'][metric_name]['original_sample']
                pvalue = stats.f_oneway(metric_data['original_sample'], other_data).pvalue
                if pvalue < 0.01:
                    accept = False
                else:
                    accept = True

                if hashed_id not in bd:
                    bd[hashed_id] = {
                        'variants': variants,
                        'metrics':[{
                            metric_name: accept,
                            'pvalue': pvalue
                        }]
                    }
                else:
                    bd[hashed_id]['metrics'].append({
                        metric_name: accept,
                        'pvalue': pvalue
                    })

    print(bd)

def breakdown():
    src_file = "/home/gerd/Workspace/synthio/experiments/consistency_data/avg_combos.json"

    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
    
    bd = dict()
    bd['bp_gadget'] = {'truths':0, 'falses':0, 'nulls':0, 'sv_truths':0, 'sv_falses':0, 'sv_nulls':0}
    bd['cg_gadget'] = {'truths':0, 'falses':0, 'nulls':0, 'sv_truths':0, 'sv_falses':0, 'sv_nulls':0}
    for hashed_id, report in existing_measurements.items():
        variants = report['variants']
        var_one = variants[0][2:]
        var_two = variants[1][2:]

        if "bp" in var_one:

            for metric_name, metric_data in report['measurements'].items():
                verdict = metric_data['accept']
                if verdict is True:
                    bd['bp_gadget']['truths'] += 1
                elif verdict is False:
                    bd['bp_gadget']['falses'] += 1
                else:
                    bd['bp_gadget']['nulls'] += 1

                if var_one == var_two:
                    if verdict is True:
                        bd['bp_gadget']['sv_truths'] += 1
                    elif verdict is False:
                        bd['bp_gadget']['sv_falses'] += 1
                    else:
                        bd['bp_gadget']['sv_nulls'] += 1
        else:

            for metric_name, metric_data in report['measurements'].items():
                verdict = metric_data['accept']
                if verdict is True:
                    bd['cg_gadget']['truths'] += 1
                elif verdict is False:
                    bd['cg_gadget']['falses'] += 1
                else:
                    bd['cg_gadget']['nulls'] += 1

                if var_one == var_two:
                    if verdict is True:
                        bd['cg_gadget']['sv_truths'] += 1
                    elif verdict is False:
                        bd['cg_gadget']['sv_falses'] += 1
                    else:
                        bd['cg_gadget']['sv_nulls'] += 1
                

    print(bd)

def means_breakdown():
    src_file = "/home/gerd/Workspace/synthio/experiments/consistency_data/avg_combos.json"

    with open(src_file, 'r+') as f:
        existing_measurements = json.load(f)
    
    bd = dict()
    bd['bp_gadget'] = {'truths':[], 'falses':[], 'nulls':[]}
    bd['cg_gadget'] = {'truths':[], 'falses':[], 'nulls':[]}

    for hashed_id, report in existing_measurements.items():
        variants = report['variants']
        var_one = variants[0][2:]
        var_two = variants[1][2:]

        if "bp" in var_one:

            for metric_name, metric_data in report['measurements'].items():
                verdict = metric_data['accept']
                if verdict is True:
                    bd['bp_gadget']['truths'].append(abs(metric_data['mean_diff']))
                elif verdict is False:
                    bd['bp_gadget']['falses'].append(abs(metric_data['mean_diff']))
                else:
                    bd['bp_gadget']['nulls'].append(abs(metric_data['mean_diff']))
        else:

            for metric_name, metric_data in report['measurements'].items():
                verdict = metric_data['accept']
                if verdict is True:
                    bd['cg_gadget']['truths'].append(abs(metric_data['mean_diff']))
                elif verdict is False:
                    bd['cg_gadget']['falses'].append(abs(metric_data['mean_diff']))
                else:
                    bd['cg_gadget']['nulls'].append(abs(metric_data['mean_diff']))

    bd['bp_gadget']['truths'] = np.mean(bd['bp_gadget']['truths']) * 100
    bd['bp_gadget']['falses'] = np.mean(bd['bp_gadget']['falses']) * 100
    bd['bp_gadget']['nulls'] = np.mean(bd['bp_gadget']['nulls']) * 100
    bd['cg_gadget']['truths'] = np.mean(bd['cg_gadget']['truths']) * 100
    bd['cg_gadget']['falses'] = np.mean(bd['cg_gadget']['falses']) * 100
    bd['cg_gadget']['nulls'] = np.mean(bd['cg_gadget']['nulls']) * 100

    print(bd)

if __name__ == "__main__":
    # big_exp()
    # report_ordering_contradictions()
    # breakdown()
    means_breakdown()