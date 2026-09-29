"""Small development-only controllers; insufficient independent smoke groups."""
import time
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

FEATURES=['log_candidates','variables','objectives','symbolic_fraction','remaining','progress','plateau','separation','uncertainty']
GRID=[-.02,0.,.02,.05,float('inf')]

def group_mean(values,groups):
    values=np.asarray(values);groups=np.asarray(groups)
    return float(np.mean([np.mean(values[groups==g]) for g in sorted(set(groups))]))

def select_threshold(scores,classic,llm,groups,grid):
    base=group_mean(llm,groups);rows=[]
    for threshold in grid:
        mask=np.asarray(scores)>threshold
        loss=group_mean(np.where(mask,llm,classic),groups)
        rows.append({'threshold':None if np.isinf(threshold) else float(threshold),'loss':loss,'escalation_rate':group_mean(mask,groups),'feasible':loss<=base+.02})
    eligible=[(i,r) for i,r in enumerate(rows) if r['feasible']]
    if eligible:idx,_=min(eligible,key=lambda ir:(ir[1]['escalation_rate'],ir[1]['loss'],ir[0]))
    else:idx,_=min(enumerate(rows),key=lambda ir:(ir[1]['loss'],ir[1]['escalation_rate'],ir[0]))
    return grid[idx],rows,rows[idx]['escalation_rate']

class GainRouter:
    def __init__(self,keys=FEATURES):self.keys=list(keys)
    def matrix(self,rows):return np.asarray([[r['features'][k] for k in self.keys] for r in rows],dtype=float)
    def _fit(self,x,y,groups):
        weights=np.asarray([1/sum(g==h for h in groups) for g in groups]);weights*=len(weights)/sum(weights)
        scaler=StandardScaler().fit(x,sample_weight=weights)
        model=Ridge(alpha=1).fit(scaler.transform(x),y,sample_weight=weights)
        return scaler,model
    def fit(self,development):
        t=time.perf_counter()
        if not development or any(r['split']!='development' for r in development):raise ValueError('fit requires development only')
        groups=[r['system_group'] for r in development]
        if len(set(groups))<2:raise ValueError('need >=2 development groups even for smoke')
        x=self.matrix(development);y=np.asarray([r['gain'] for r in development]);oof=np.zeros(len(y))
        for g in sorted(set(groups)):
            train=np.asarray([h!=g for h in groups]);valid=~train
            scale,model=self._fit(x[train],y[train],np.asarray(groups)[train].tolist())
            oof[valid]=model.predict(scale.transform(x[valid]))
        self.threshold,self.curve,self.rate=select_threshold(oof,[r['classical_loss'] for r in development],[r['llm_loss'] for r in development],groups,GRID)
        self.scaler,self.model=self._fit(x,y,groups);self.training_groups=sorted(set(groups));self.fit_seconds=time.perf_counter()-t
        self.oof=oof.tolist();return self
    def predict(self,predecision_rows):return self.model.predict(self.scaler.transform(self.matrix(predecision_rows)))
    def export(self):return {'features':self.keys,'training_groups':self.training_groups,'threshold':None if np.isinf(self.threshold) else float(self.threshold),'development_oof_rate':self.rate,'development_curve':self.curve,'development_oof_predictions':self.oof,'coefficient':self.model.coef_.tolist(),'intercept':float(self.model.intercept_),'mean':self.scaler.mean_.tolist(),'scale':self.scaler.scale_.tolist(),'fit_seconds':self.fit_seconds,'evidence':'insufficient: two development systems, one held-out smoke system'}

class UncertaintyRouter:
    def fit(self,development):
        if any(r['split']!='development' for r in development):raise ValueError('fit requires development only')
        values=[r['features']['uncertainty'] for r in development]
        grid=list(np.quantile(values,[0,.25,.5,.75,1]))+[float('inf')]
        self.threshold,self.curve,self.rate=select_threshold(values,[r['classical_loss'] for r in development],[r['llm_loss'] for r in development],[r['system_group'] for r in development],grid)
        self.grid=grid;return self
    def predict(self,rows):return np.asarray([r['features']['uncertainty'] for r in rows])
