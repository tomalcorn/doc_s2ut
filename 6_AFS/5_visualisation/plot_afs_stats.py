import matplotlib.pyplot as plt

# Sample data (replace these with your actual data)
l0_values = ['low', 'medium', 'high']  # Categorical variable (replace with actual categories)
wer_values = [0.15, 0.10, 0.08]        # WER values corresponding to l0_values
features_kept = [90, 70, 50]           # % of features kept corresponding to l0_values

fig, ax1 = plt.subplots()

# Plot WER on the first y-axis
color = 'tab:blue'
ax1.set_xlabel('l_0 Regularizer')
ax1.set_ylabel('WER', color=color)
ax1.plot(l0_values, wer_values, color=color, marker='o', label='WER')
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('% Features Kept', color=color)
ax2.plot(l0_values, features_kept, color=color, marker='o', label='Features Kept')
ax2.tick_params(axis='y', labelcolor=color)

# Title and legend
plt.title('WER and % Features Kept vs l_0 Regularizer')
fig.tight_layout()  # Adjust layout to avoid overlap
plt.show()
