# KPI Dictionary (for tooltips)

Revenue = SUM(units * price_gbp)  
Gross Profit = SUM(units * (price_gbp - unit_cost_gbp))  
Promo Revenue Share = promo revenue / total revenue  
Incremental Units = promo units - baseline units (median non-promo units per store-item)  
Incremental GP = incremental units * (regular_price - unit_cost)  
ROI Proxy = incremental GP / discount cost  
Discount Cost (proxy) = baseline_units * discount_depth * regular_price  
Price Elasticity = coefficient of log(price) in log-log regression of units  
Stockout Rate = % rows with stockout_flag = 1
