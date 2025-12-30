import matplotlib.pyplot as plt
import numpy as np
avg_remain_info = [0.24766699999999994, 0.16949899999999998, 0.12006300000000003]
# Confidence probabilities for 3 streets (e.g., preflop, flop, turn/river)
confidence_probs = np.array([
    [0.04,  0.076, 0.126, 0.168, 0.212, 0.267, 0.321, 0.362, 0.425, 0.495, 0.566, 0.635,
     0.693, 0.759, 0.821, 0.866, 0.895, 0.921, 0.948, 1.0],
    [0.075, 0.15,  0.208, 0.258, 0.308, 0.358, 0.405, 0.479, 0.548, 0.611, 0.657, 0.693,
     0.724, 0.751, 0.778, 0.802, 0.82,  0.843, 0.861, 1.0],
    [0.094, 0.176, 0.258, 0.32,  0.403, 0.453, 0.517, 0.589, 0.63,  0.666, 0.712, 0.741,
     0.766, 0.785, 0.803, 0.818, 0.836, 0.85,  0.86, 1.0]
])

lin_space = np.linspace(0, 1.9, confidence_probs.shape[1])

x = [lin_space * avg_remain_info[0], lin_space * avg_remain_info[1], lin_space * avg_remain_info[2]]  # X-axis represents normalized winrate or similar metric

# Plotting
plt.figure(figsize=(10, 6))
labels = ['Preflop', 'Flop', 'Turn/River']
for i, probs in enumerate(confidence_probs):
    plt.plot(x[i], probs, label=labels[i], marker='o')

plt.title('CDF of deviation by Street')
plt.xlabel('Deviation: |p(4) - p(i)|')
plt.ylabel('CDF of deviation')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
