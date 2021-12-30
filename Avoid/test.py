import time
import numpy as np
import tensorflow.keras as keras
from avoid2 import Avoid


width = 300
height = 400

model = keras.models.load_model("./Avoid/models/avoidPoop_cnn.h5")
env = Avoid(width, height)

stepSum = 0
for i in range(10):
    score = 0
    state = env.reset()

    for _ in range(2000):
        actions = model.predict(np.reshape(state, [1, 30, 30, 1]))
        action = np.argmax(actions)
        state, reward, done = env.step(action)

        score += reward
        if done:
            break

        time.sleep(0.03)

    print(score)
