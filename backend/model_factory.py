import pymc as pm
import pytensor.tensor as pt
import numpy as np

def build_dynamic_pymc_model(Y_obs, parsed_levels):
    with pm.Model() as model:
        global_mean = pm.Normal('global_mean', mu=np.mean(Y_obs), sigma=np.std(Y_obs))
        mu_rows = global_mean
        
        for level_idx in sorted(parsed_levels.keys()):
            lvl = parsed_levels[level_idx]
            name = lvl["name"]
            
            sigma_level = pm.HalfNormal(f'sigma_{name}', sigma=5)
            z_level = pm.Normal(f'z_{name}', mu=0, sigma=1, shape=lvl["n_nodes"])
            node_offsets = pm.Deterministic(f'offset_{name}', z_level * sigma_level)
            
            level_effect = node_offsets[lvl["idx"]]
            
            if lvl["X"] is not None:
                for i, cov_name in enumerate(lvl["cov_names"]):
                    beta = pm.Normal(f'beta_{cov_name}', mu=0, sigma=5)
                    level_effect += lvl["X"][:, i] * beta
                    
            mu_rows += level_effect
            
        # 观测层：Student-T 分布抓取厚尾异常值
        sigma_obs = pm.HalfNormal('sigma_obs', sigma=5)
        pm.StudentT('Y_est', nu=3.5, mu=mu_rows, sigma=sigma_obs, observed=Y_obs)
        
    return model

def run_mcmc_sampling(model):
    with model:
        # 使用 numpyro 激活 GPU/多核加速
        trace = pm.sample(draws=1500, tune=1000, target_accept=0.9, nuts_sampler="numpyro", return_inferencedata=True)
    return trace