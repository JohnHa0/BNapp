import pymc as pm
import pytensor.tensor as pt
import numpy as np

def build_dynamic_pymc_model(Y_obs, parsed_levels):
    y_std = max(np.std(Y_obs), 1e-5)
    with pm.Model() as model:
        global_mean = pm.Normal('global_mean', mu=np.mean(Y_obs), sigma=y_std)
        mu_rows = global_mean
        
        for level_idx in sorted(parsed_levels.keys()):
            lvl = parsed_levels[level_idx]
            name = lvl["name"]
            
            sigma_level = pm.HalfNormal(f'sigma_{name}', sigma=y_std)
            z_level = pm.Normal(f'z_{name}', mu=0, sigma=1, shape=lvl["n_nodes"])
            node_offsets = pm.Deterministic(f'offset_{name}', z_level * sigma_level)
            
            level_effect = node_offsets[lvl["idx"]]
            
            if lvl["X"] is not None:
                for i, cov_name in enumerate(lvl["cov_names"]):
                    beta = pm.Normal(f'beta_{cov_name}', mu=0, sigma=y_std)
                    level_effect += lvl["X"][:, i] * beta
                    
            mu_rows += level_effect
            
        # 观测层：Student-T 分布抓取厚尾异常值
        sigma_obs = pm.HalfNormal('sigma_obs', sigma=y_std)
        pm.StudentT('Y_est', nu=3.5, mu=mu_rows, sigma=sigma_obs, observed=Y_obs)
        
    return model

def run_mcmc_sampling(model, sampling_mode="fast", custom_draws=None, custom_tune=None):
    with model:
        # 优先使用用户自定义参数，否则根据模式选择预设
        if custom_draws and custom_tune:
            draws, tune = custom_draws, custom_tune
        elif sampling_mode == "fast":
            draws, tune = 500, 300
        else:
            draws, tune = 1500, 1000
            
        # 尝试使用 JAX (Numpyro) 加速采样，如果不可用或版本冲突则回退到标准 NUTS
        # 捕捉 Exception 而非 ImportError，因为 JAX 版本不匹配（如 jaxlib > jax）会抛出 RuntimeError
        try:
            import numpyro
            import jax
            # 验证 jax 能够正常工作，防止版本不一致导致的初始化失败
            _ = jax.devices()
            nuts_sampler = "numpyro"
        except Exception:
            nuts_sampler = "pymc"

        trace = pm.sample(
            draws=draws, 
            tune=tune, 
            target_accept=0.9, 
            return_inferencedata=True, 
            cores=1, 
            progressbar=True,
            nuts_sampler=nuts_sampler
        )
        pm.sample_posterior_predictive(trace, extend_inferencedata=True, progressbar=True)
    return trace