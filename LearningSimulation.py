import torch
import torch.optim as optim
import torch.nn.functional as F
from Models import CarNN
import gymnasium as gym
from gymnasium.wrappers import GrayScaleObservation, ResizeObservation
import numpy as np

gym.envs.registration.register(
    id='ChaosCarGameEnv',
    entry_point='CarGameEnv:CarGameEnv',
)

env = GrayScaleObservation(gym.make('ChaosCarGameEnv'), keep_dim=False)
env = ResizeObservation(env, shape=84)

state_shape = env.observation_space.shape
action_dim = env.action_space.n

model = CarNN(state_shape, action_dim)
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
for epoch in range(num_epochs):
    state_tuple = env.reset()
    state_np = state_tuple[0]
    done = False
    while not done:
        # Add batch and channel dimension since it is grey scale
        state_tensor = torch.tensor(state_np).unsqueeze(0).unsqueeze(0).float() / 255.0 
    
        action_prob = model(state_tensor)
        print(f"LearningSimulation --> Action probabilities: {action_prob}")
        action = torch.argmax(action_prob, dim=1).item()
        # print(f"LearningSimulation --> Action: {action}")
        next_state, reward, done, _, _ = env.step(action)
        state = next_state

        optimizer.zero_grad()
        print(f"LearningSimulation --> Action: {action}, Reward: {reward}")
        loss = -torch.log(action_prob[0, action]) * reward
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch + 1} completed')
    env.render()

env.close()
