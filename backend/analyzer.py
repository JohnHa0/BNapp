import arviz as az
import numpy as np

def extract_insights(trace, Y_obs, node_names):
    # Retrieve expected predicted values from the posterior predictive check
    posterior_mu = trace.posterior_predictive['Y_est'].mean(dim=["chain", "draw"]).values
    deviations = Y_obs - posterior_mu
    std_dev = np.std(deviations)
    
    # Extract PPC for density plots
    try:
        ppc_samples = trace.posterior_predictive['Y_est'].values.flatten()
        # Randomly subsample PPC to keep payload size small
        if len(ppc_samples) > 2000:
            ppc_subsample = np.random.choice(ppc_samples, size=2000, replace=False).tolist()
        else:
            ppc_subsample = ppc_samples.tolist()
    except KeyError:
        ppc_subsample = []

    ppc_data = {
        "y_actual": [float(y) for y in Y_obs if not np.isnan(y)],
        "y_predictive": [float(y) for y in ppc_subsample if not np.isnan(y)]
    }
    
    perf_data = []
    for i in range(len(Y_obs)):
        dev = deviations[i]
        status = "Average"
        if dev > 2 * std_dev: status = "Bright Spot"
        elif dev < -2 * std_dev: status = "Dark Spot"
        
        perf_data.append({
            "NodeName": str(node_names[i]),
            "Expected": float(posterior_mu[i]),
            "Deviation": float(dev),
            "Actual": float(Y_obs[i]),
            "Status": status
        })
        
    summary = az.summary(trace, filter_vars="like", var_names=["beta_"], hdi_prob=0.95)
    summary_df = summary[['mean', 'hdi_2.5%', 'hdi_97.5%', 'r_hat', 'ess_bulk']].rename(
        columns={'hdi_2.5%': 'hdi_3%', 'hdi_97.5%': 'hdi_97%'}
    ).to_dict(orient="index")
    
    # Extract clean beta dictionary for what-if simulator
    betas = {k.replace('beta_', ''): float(v['mean']) for k, v in summary_df.items()}
    
    return perf_data, summary_df, ppc_data, betas