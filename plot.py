import pickle
import matplotlib.pyplot as plt

with open('score.txt', 'rb') as f:
    Y, X = pickle.load(f)
print(Y)
print(X)
print(len(Y))
plt.plot(list(range(X)), Y)
plt.show()