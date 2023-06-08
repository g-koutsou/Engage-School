from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import xmltodict

data = dict()
for y in range(1993, 2023):
    for m in [6, 11]:
        if (y, m) == (2020, 11):
            continue
        fname = "TOP500_{}{:02.0f}_all.xml".format(y, m)
        try:
            d = xmltodict.parse(open(fname, "r").read())
        except FileNotFoundError:
            break
        t001 = np.array([x['top500:r-max'] for x in d['top500:list']['top500:site'][:1]], float)
        t010 = np.array([x['top500:r-max'] for x in d['top500:list']['top500:site'][:10]], float)
        t100 = np.array([x['top500:r-max'] for x in d['top500:list']['top500:site'][:100]], float)
        data[m, y] = (t001/1e6, t010/1e6, t100/1e6)

plt.rcParams['axes.prop_cycle'].by_key()['color']
fig = plt.figure(1, figsize=(4,3))
fig.clf()
ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
ax.set_yscale("log")
ym = sorted([(y,m) for m,y in data.keys()])
xx = np.array([y+m/12 for y,m in ym])
top001 = np.array([data[m, y][0].sum() for y,m in ym])
top010 = np.array([data[m, y][1].sum() for y,m in ym])
top100 = np.array([data[m, y][2].sum() for y,m in ym])
ax.plot(xx, top001, ls="", marker="s", ms=4, label="Top system")
ax.plot(xx, top010, ls="", marker="o", ms=4, label="Sum of top 10 systems")
ax.plot(xx, top100, ls="", marker="^", ms=4, label="Sum of top 100 systems")
ax.set_ylabel("$R_{max}$ [Pflop/s]")
ax.set_xlabel("Year")
ax.legend(loc="upper left", frameon=False)
fig.show()
fig.patch.set_facecolor(None)
fig.patch.set_alpha(0)
fig.savefig("top500.png", bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)

