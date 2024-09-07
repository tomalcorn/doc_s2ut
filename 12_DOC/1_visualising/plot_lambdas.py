import matplotlib.pyplot as plt

lambdas = [n/10 for n in range(11)]

bleu_scores = [12.36, 12.37, 12.27, 12.31, 12.37, 12.30, 12.22, 12.29, 12.19, 12.20, 12.21]
comet_scores = [48.42, 48.65, 48.47, 48.43, 48.61, 48.54, 48.54, 48.54, 48.46, 48.38, 48.42]

bleu_noprefix = [3.26, 3.33, 3.24, 3.33, 3.29, 3.35, 3.39, 3.29, 3.40, 3.30, 3.20]
comet_noprefix = [44.51, 44.58, 44.51, 44.39, 44.36, 44.44, 44.64, 44.64, 44.48, 44.47, 44.60]

fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True, figsize=(12, 10))


ax1.plot(lambdas, bleu_scores, marker='o', color="tab:blue", label="Bleu score")
ax2 = ax1.twinx()
ax2.plot(lambdas, comet_scores, marker='v', color='tab:orange', label="Comet score")

ax3.plot(lambdas, bleu_noprefix, marker='o', color='tab:blue', label="Bleu score")
ax4 = ax3.twinx()
ax4.plot(lambdas, comet_noprefix, marker='v', color='tab:orange', label="Comet score")

# Adding the legend to the plots
ax1.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=16)
ax2.legend(loc='upper right', bbox_to_anchor=(1, 0.87), fontsize=16)

# Adding title and axis labels
fig.suptitle("BLEU and COMET Scores with and without prefix", fontsize=22)
ax3.set_xlabel("$\gamma$", fontsize=20)
ax3.tick_params(axis='x', labelsize = 16)
ax1.set_ylabel("BLEU Score", fontsize=20)
ax1.tick_params(axis='y', labelsize = 16)
ax2.set_ylabel("COMET Score", fontsize=20)
ax2.tick_params(axis='y', labelsize = 16)
ax3.set_ylabel("BLEU Score (No Prefix)", fontsize=20)
ax3.tick_params(axis='y', labelsize = 16)
ax4.set_ylabel("COMET Score (No Prefix)", fontsize=20)
ax4.tick_params(axis='y', labelsize = 16)

# plt.show()
plt.tight_layout()
plt.savefig("/Users/tomalcorn/Desktop/lambda_graph.pdf")
