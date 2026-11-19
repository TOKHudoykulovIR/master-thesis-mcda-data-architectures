const C = require('../src/core.js');
const M = {C1:{TTDP:2,AIRD:4,PORT:2,TCO:3,SECC:3},C2:{TTDP:2,AIRD:3,PORT:5,TCO:3,SECC:2},C3:{TTDP:4,AIRD:4,PORT:2,TCO:3,SECC:3},
C4:{TTDP:4,AIRD:3,PORT:5,TCO:3,SECC:2},C5:{TTDP:2,AIRD:4,PORT:2,TCO:3,SECC:4},C6:{TTDP:4,AIRD:3,PORT:5,TCO:3,SECC:2},C7:{TTDP:2,AIRD:4,PORT:4,TCO:3,SECC:2}};
const W = [[0.2,0.2,0.2,0.2,0.2],[0.1,0.1,0.2,0.1,0.5],[0.35,0.3,0.1,0.15,0.1],[0.05,0.1,0.6,0.1,0.15]];
const out = {topsis:[], floor:[], frontier:null, smaa:null, smaaFloor:null};
for (const w of W) {
  out.topsis.push(C.closeness(C.activeModel(M,{floor:false,includeC7:true}).X, w));
  out.floor.push(C.closeness(C.activeModel(M,{floor:true,includeC7:true}).X, w));
}
const mdl = C.activeModel(M,{floor:false,includeC7:true});
out.frontier = C.frontier(mdl, W[1], 'SECC', 'PORT', 50).grid;
out.smaa = C.smaa(mdl, {type:'uniform'}, {k:20000, seed:7, tcoUncertainty:true}).acceptability;
out.smaaFloor = C.smaa(C.activeModel(M,{floor:true,includeC7:true}), {type:'uniform'}, {k:20000, seed:7, tcoUncertainty:true}).acceptability;
const Wp=[[0.1,0.15,0.2,0.15,0.4],[0.12,0.1,0.25,0.13,0.4],[0.08,0.2,0.15,0.17,0.4],[0.1,0.1,0.3,0.1,0.4],[0.15,0.15,0.1,0.2,0.4],[0.1,0.12,0.18,0.2,0.4]];
out.mom = C.dirichletMoM(Wp);
out.smaaPanel = C.smaa(mdl, {type:'dirichlet', alpha: out.mom}, {k:20000, seed:3, tcoUncertainty:true}).acceptability;
console.log(JSON.stringify(out));
