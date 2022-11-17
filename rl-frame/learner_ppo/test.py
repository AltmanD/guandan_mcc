import numpy as np

np.set_printoptions(threshold=np.inf)
b = np.load("/home/luyd/guandan_mcc/rl-frame/learner_ppo/test.npy", allow_pickle=True).item()
print(b)
for k,v in b.items():
    print(k,v.shape)
    if np.nan in v:
        print('have nan')
print(b.keys())
