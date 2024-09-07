import matplotlib.pyplot as plt

# Sample data
l0_values = [x/10 for x in range(1, 9)]  # l_0 regularizer values
wer_values = [21.79, 23.83, 26.06, 28.25, 30.37, 31.76, 33.53, 37.21]  # WER values 
kept_pcent = [45.12, 27.30, 25.07, 21.59, 21.46, 20.31, 16.68, 15.73] # % Features Kept
wer_values_avg = [19.46, 20.99, 22.42, 24.43, 25.54, 27.06, 28.50, 29.56]  # WER values avg
kept_pcent_avg = [45.24, 30.82, 26.84, 23.96, 22.09, 20.33, 18.48, 17.] # % Features Kept avg
sparsity_rate = [100 - x for x in kept_pcent]  
sparsity_rate_avg = [100 - x for x in kept_pcent_avg]  

fig, ax1 = plt.subplots(figsize=(9, 6.5))

# Plot WER on the first y-axis
color = 'tab:blue'
ax1.set_xlabel('$\lambda$', fontsize=16)
ax1.set_ylabel('WER', fontsize=16)
ax1.plot(l0_values, wer_values, color=color, marker='o', label='WER')
ax1.plot(l0_values, wer_values_avg, color=color, marker='x', label='WER avg')
ax1.tick_params(axis='y', labelsize=12)
ax1.tick_params(axis='x', labelsize=12)

# Plot ASR pre-train
plt.axhline(y=17.44, color='blue', linestyle="dashed", label='ASR baseline WER')

# Create a second y-axis
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Sparsity Rate', fontsize=16)
ax2.plot(l0_values, sparsity_rate, color=color, marker='o', label='Sparsity Rate')
ax2.plot(l0_values, sparsity_rate_avg, color=color, marker='x', label='Sparsity Rate avg')
ax2.tick_params(axis='y', labelsize=12)

# Set the range for % Features Kept y-axis
ax2.set_ylim(0, 100)
ax1.set_ylim(0, 100)

ax1.grid(which="both")
# Title and legend
plt.title('WER and Sparsity Rate vs $\lambda$', fontsize=18)
fig.tight_layout()  # Adjust layout to avoid overlap

# Add legends for both lines
ax1.legend(loc='center right', bbox_to_anchor=(1, 0.64), fontsize=12)
ax2.legend(loc='center right', bbox_to_anchor=(1, 0.50), fontsize=12)

plt.savefig("/Users/tomalcorn/Desktop/afs_stats.pdf", dpi=500)
# plt.show()
