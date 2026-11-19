import json, sys, numpy as np
sys.path.insert(0, '/mnt/user-data/outputs/engine')
from engine import topsis, smaa, CRITERIA, CONFIGS
from engine.matrix import PerformanceModel, secc_floor
from engine.frontier import frontier
js = json.load(open('test/js_out.json'))
M = {'C1':dict(TTDP=2,AIRD=4,PORT=2,TCO=3,SECC=3),'C2':dict(TTDP=2,AIRD=3,PORT=5,TCO=3,SECC=2),'C3':dict(TTDP=4,AIRD=4,PORT=2,TCO=3,SECC=3),
'C4':dict(TTDP=4,AIRD=3,PORT=5,TCO=3,SECC=2),'C5':dict(TTDP=2,AIRD=4,PORT=2,TCO=3,SECC=4),'C6':dict(TTDP=4,AIRD=3,PORT=5,TCO=3,SECC=2),'C7':dict(TTDP=2,AIRD=4,PORT=4,TCO=3,SECC=2)}
model = PerformanceModel(M); model.apply_tco_k11(3,3)
ben = model.benefit()
W = [[0.2]*5,[0.1,0.1,0.2,0.1,0.5],[0.35,0.3,0.1,0.15,0.1],[0.05,0.1,0.6,0.1,0.15]]
md = 0
for i,w in enumerate(W):
    c = topsis.closeness(model.X(), w, ben); md = max(md, np.abs(c-np.array(js['topsis'][i])).max())
    fm,_ = secc_floor(model); c = topsis.closeness(fm.X(), w, ben); md = max(md, np.abs(c-np.array(js['floor'][i])).max())
print('TOPSIS max abs diff (incl. floor):', md)
_,_,g = frontier(model, W[1], 'SECC', 'PORT', 50)
print('frontier cells differing:', int((g != np.array(js['frontier'])).sum()), 'of', g.size)
uni = lambda rng,k: rng.dirichlet(np.ones(5), k)
r = smaa.run(model, uni, k=20000, seed=1)
print('SMAA uniform max abs diff in acceptability:', np.abs(r['acceptability']-np.array(js['smaa'])).max().round(4))
fm,_ = secc_floor(model); r = smaa.run(fm, uni, k=20000, seed=1)
print('SMAA floor max abs diff:', np.abs(r['acceptability']-np.array(js['smaaFloor'])).max().round(4))
Wp=np.array([[0.1,0.15,0.2,0.15,0.4],[0.12,0.1,0.25,0.13,0.4],[0.08,0.2,0.15,0.17,0.4],[0.1,0.1,0.3,0.1,0.4],[0.15,0.15,0.1,0.2,0.4],[0.1,0.12,0.18,0.2,0.4]])
print('Dirichlet MoM diff:', np.abs(smaa.dirichlet_mom(Wp)-np.array(js['mom'])).max())
r = smaa.run(model, smaa.weight_sampler_dirichlet(Wp), k=20000, seed=2)
print('SMAA panel-mode max abs diff:', np.abs(r['acceptability']-np.array(js['smaaPanel'])).max().round(4))
print('engine first-rank uniform:', dict(zip(model.configs, np.round(smaa.run(model, uni, k=20000, seed=1)['first_rank'],3))))
