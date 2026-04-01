import arviz as az
import numpy as np

def extract_insights(trace, Y_obs, node_names):
    posterior_mu = trace.posterior['Y_est'].mean(dim=["chain", "draw"]).values
    deviations = Y_obs - posterior_mu
    std_dev = np.std(deviations)
    
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
    summary_df = summary[['mean', 'hdi_2.5%', 'hdi_97.5%']].rename(columns={'hdi_2.5%': 'hdi_3%', 'hdi_97.5%': 'hdi_97%'}).to_dict(orient="index")
    
    return perf_data, summary_df