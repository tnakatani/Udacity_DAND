treatment_df = df2.query('group == "treatment"')
treatment_convert = treatment_df.query('converted =="1"').count()[0] / treatment_df.converted.shape[0]
treatment_convert

control_df = df2.query('group == "control"')
control_convert = control_df.converted.mean() #.query('converted == "1"').count()[0] / control_df.shape[0]
control_convert

df2[(df2['group'] == 'treatment')]['converted'].mean() - df2[(df2['group'] == 'control')]['converted'].mean()
