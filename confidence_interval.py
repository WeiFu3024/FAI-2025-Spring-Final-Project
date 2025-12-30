avg_remain_info = [0.24766699999999994, 0.16949899999999998, 0.12006300000000003]
confidence_probabilities = [
 [0.04,  0.076, 0.126, 0.168, 0.212, 0.267, 0.321, 0.362, 0.425, 0.495, 0.566, 0.635,
  0.693, 0.759, 0.821, 0.866, 0.895, 0.921, 0.948, 1.,   ],
 [0.075, 0.15,  0.208, 0.258, 0.308, 0.358, 0.405, 0.479, 0.548, 0.611, 0.657, 0.693,
  0.724, 0.751, 0.778, 0.802, 0.82,  0.843, 0.861, 1.,   ],
 [0.094, 0.176, 0.258, 0.32,  0.403, 0.453, 0.517, 0.589, 0.63,  0.666, 0.712, 0.741,
  0.766, 0.785, 0.803, 0.818, 0.836, 0.85,  0.86,  1.,   ]
  ]
BINS = 20

def find_confidence_interval(avg_remain_info, confidence_probabilities, confidence_rate):
    """
    Find the confidence interval for a given win rate.
    
    :param win_rate: The win rate to find the confidence interval for.
    :param avg_remain_info: The average remaining information.
    :param confidence_probabilities: The confidence probabilities.
    :return: The confidence interval as a tuple (lower_bound, upper_bound).
    """
    coeficients = []
    for i in range(len(avg_remain_info)):
        for j in range(len(confidence_probabilities[0])-1):
            if confidence_probabilities[i][j] <= confidence_rate <= confidence_probabilities[i][j + 1]:
                deviation_left = confidence_rate - confidence_probabilities[i][j]
                deviation_right = confidence_probabilities[i][j + 1] - confidence_rate
                interpolated_k = (deviation_left * (j + 1) + deviation_right * j) / (deviation_left + deviation_right)
                coeficients.append(interpolated_k * avg_remain_info[i] / BINS * 2)
                break
            if confidence_probabilities[i][BINS-1] <= confidence_rate:
                coeficients.append(avg_remain_info[i] * 1.9)
                break    
    return coeficients

print("Confidence Interval Coefficients 0.4:", find_confidence_interval(avg_remain_info, confidence_probabilities, 0.4))
print("Confidence Interval Coefficients 0.6:", find_confidence_interval(avg_remain_info, confidence_probabilities, 0.6))