import matplotlib.pyplot as plt
import json
import matplotlib.patches as mpatches
import matplotlib.ticker as plticker
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as mtick

def knobs():
    # do some plotting
    
    data = []
    key = "br-miss-rate_c1"
    src_file = "/home/gerd/Workspace/synthio/experiments/knobs_data.json"

    with open(src_file, 'r+') as f:
        data = json.load(f)

    values = data[key]
    
    lop_1_values = values['lopside_0']
    lop_2_values = values['lopside_1']
    lop_3_values = values['lopside_2']
    cpi_1_values = data['cpi']['lopside_0']
    cpi_2_values = data['cpi']['lopside_1']
    cpi_3_values = data['cpi']['lopside_2']

    plt.rcParams["figure.figsize"] = (9,6)
    plt.rcParams['figure.constrained_layout.use'] = True

    fig, ax = plt.subplots(1,1)

    ax.scatter([l * 100 for l in lop_1_values], range(1, len(lop_1_values)+1), label = 'LOPSIDE = 0', color = 'green', alpha=0.5, s = [200 * v **2 for v in cpi_1_values])
    ax.scatter([l * 100 for l in lop_2_values], range(1, len(lop_2_values)+1), label = 'LOPSIDE = 1', color = 'blue', alpha=0.5, s = [200 * v ** 2 for v in cpi_2_values])
    ax.scatter([l * 100 for l in lop_3_values], range(1, len(lop_3_values)+1), label = 'LOPSIDE = 2', color = 'purple', alpha=0.5, s = [200 * v ** 2 for v in cpi_3_values])


    gpatch =  Line2D([0], [0], marker='o', color='w', label='LOPSIDE = 0', alpha = 0.5,
                        markerfacecolor='g', markersize=30)
    bpatch =  Line2D([0], [0], marker='o', color='w', label='LOPSIDE = 1',alpha = 0.5,
                        markerfacecolor='b', markersize=30)
    ppatch =  Line2D([0], [0], marker='o', color='w', label='LOPSIDE = 2',alpha = 0.5,
                        markerfacecolor='purple', markersize=30)

    new_handles = [gpatch, bpatch, ppatch]

    ax.legend(handles = new_handles,labelspacing=2.5, borderpad=1.5, loc="lower left")

    ax.set_yticks([])
    ax.set_xlim([5.0, max([l * 100 for l in lop_1_values]) + 1])
    loc = plticker.MultipleLocator(base=0.5) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.set_xlabel("Branch Misprediction Rate (%)", fontsize = 16, labelpad=16)

    fname = "/home/gerd/Workspace/synthio/experiments/" + "knobs_plot.png"

    # plt.show()
    plt.savefig(fname, dpi=150)

def imbp():
    data = []
    key = "bp_gadget_c6"
    src_file = "/home/gerd/Workspace/synthio/experiments/skylake_im.json"

    with open(src_file, 'r+') as f:
        data = json.load(f)

    data = data[key]
    br_mr = data['br-miss-rate']
    cpi = data['cpi']
    br_cnd = data['br-conditionals-miss-rate']

    fig, ax = plt.subplots(3, figsize=(14,12), constrained_layout=True)
    plt.rcParams["font.size"] = 16

    data = [x * 100 for x in br_mr]

    ax[0].hist(data, bins = 50, color = 'green', edgecolor = 'black', label = 'All branches')
    handles, labels = ax[0].get_legend_handles_labels()
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 50'))
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[0].legend(handles = handles, loc="upper left")
    ax[0].set_xlabel("Misprediction Rate (%)", fontsize = 16, labelpad=16)


    ax[1].hist([x * 100 for x in br_cnd], bins = 50, color = 'blue', edgecolor = 'black', label = 'Conditional Branches')
    handles, labels = ax[1].get_legend_handles_labels()
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 50')) 
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[1].legend(handles = handles, loc="upper left")
    ax[1].set_xlabel("Misprediction Rate (%)", fontsize = 16, labelpad=16)

    ax[2].hist(cpi, bins = 50, color = 'red', edgecolor = 'black', label = 'Cycles per Instruction (CPI)')
    handles, labels = ax[2].get_legend_handles_labels()    
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 50'))
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[2].legend(handles = handles, loc="upper right")
    ax[2].set_xlabel("Cycles per Instructions (CPI)", fontsize = 16, labelpad=16)

    # fig.supxlabel("Misprediction Rate (%)")
    fig.supylabel("Count")

    fname = "/home/gerd/Workspace/synthio/experiments/" + "bp_im_paper.png"
    plt.savefig(fname, dpi=150)

def imcg():
    data = []
    key = "cache_gadget_c2"
    src_file = "/home/gerd/Workspace/synthio/experiments/skylake_im.json"

    with open(src_file, 'r+') as f:
        data = json.load(f)

    data = data[key]
    l1_load = data['l1-load-miss-rate']
    l2_load = data['l2-load-miss-rate']
    cpi = data['cpi']
    

    fig, ax = plt.subplots(3, figsize=(14,12), constrained_layout=True)
    plt.rcParams["font.size"] = 16


    ax[0].hist([x * 100 for x in l1_load], bins = 20, color = 'green', edgecolor = 'black', label = 'L1 Cache - Loads')
    handles, labels = ax[0].get_legend_handles_labels()
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 20'))
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[0].legend(handles = handles, loc="upper center")
    ax[0].set_xlabel("Miss Rate (%)", fontsize = 16, labelpad=16)


    ax[1].hist([x * 100 for x in l2_load], bins = 20, color = 'blue', edgecolor = 'black', label = 'L2 Cache - Loads')
    handles, labels = ax[1].get_legend_handles_labels()
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 20')) 
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[1].legend(handles = handles, loc="upper left")
    ax[1].set_xlabel("Miss Rate (%)", fontsize = 16, labelpad=16)

    ax[2].hist(cpi, bins = 20, color = 'red', edgecolor = 'black', label = 'Cycles per Instruction (CPI)')
    handles, labels = ax[2].get_legend_handles_labels()    
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Bins = 20'))
    handles.append(mpatches.Patch(color = 'grey', label = 'Number of Data Points = 100')) 
    ax[2].legend(handles = handles, loc="upper left")
    ax[2].set_xlabel("Cycles per Instructions (CPI)", fontsize = 16, labelpad=16)

    # fig.supxlabel("Misprediction Rate (%)")
    fig.supylabel("Count")

    fname = "/home/gerd/Workspace/synthio/experiments/" + "cg_im_paper.png"
    plt.savefig(fname, dpi=150)

def set_axis_style(ax, labels):
    ax.set_xticks(np.arange(1, len(labels) + 1), labels=labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    # ax.set_xlabel('Environment (Intel x86)')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # ax.set_yscale('log')
    # ax.set_ylim(0.97,1.02)

def plot_violins():
    
    data = None
    with open('/home/gerd/Workspace/synthio/experiments/reproducibility_data/violin.json', 'r+') as f:
        data = json.load(f)

    plt.rcParams.update({'font.size': 16})
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(16, 10))

    fig.supylabel("L1 Load Miss-Rate (%)", weight=550,x='0.005', ha='left')
    fig.supxlabel("Environment (Intel x86)", weight=550, va='bottom')

    #Plot some metric
    # variant = 'bp_gadget_c1'
    # metric = 'br-miss-rate'
    variant = 'cache_gadget_c1'
    metric = 'l1-load-miss-rate'
    envs = ["skylake", "haswell", "kabylake", "broadwell"]

    
    for i in range(0,4):
        # ax.set_title('Comparison across four different environments for variant 1 of the BranchPrediction Gadget')
        # ax[i].set_ylabel('Branch Misprediction Rate in % (All Branches)')
        
        to_plot = list()
        labels = list()
        for env, values in data[variant][metric].items():
            if env != envs[i]:
                continue

            labels.append(env)
            to_plot.append([x * 100 if x != 0 else x for x in values[:20]])

        parts = ax[i].violinplot(to_plot, showextrema=True, points=50)

        for pc in parts['bodies']:
            pc.set_facecolor('#FFA024')
            pc.set_edgecolor('#FF8000')
            pc.set_alpha(1)

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            if not partname in parts:
                continue
            vp = parts[partname]
            vp.set_edgecolor("#251504")
            vp.set_linewidth(1)

        quartile1, medians, quartile3 = np.percentile(to_plot, [25, 50, 75], axis=1)
        inds = np.arange(1, len(medians) + 1)
        ax[i].vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=20)
    
        ax[i].scatter(inds, medians, marker='o', color='#fafafa', s=10, zorder=3)
    
        set_axis_style(ax[i], labels)

    fig.tight_layout()
    plt.savefig("violin_one", dpi=150)

if __name__ == "__main__":
    plot_violins()
    