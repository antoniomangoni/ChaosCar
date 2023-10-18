import torch
import torch.optim as optim
import torch.nn.functional as F
from Models import CarNN
import gymnasium as gym
import numpy as np

gym.envs.registration.register(
    id='ChaosCarGameEnv',
    entry_point='CarGameEnv:CarGameEnv',
)

env = gym.make('ChaosCarGameEnv')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
model = CarNN(state_dim, action_dim)
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
for epoch in range(num_epochs):
    state_tuple = env.reset()
    state_np = state_tuple[0]
    done = False
    while not done:
        state_tensor = torch.tensor(state_np)
        action_prob = model(state_tensor)
        action = torch.argmax(action_prob).item()
        next_state, reward, done, _ = env.step(action)
        state = next_state

        optimizer.zero_grad()
        loss = -torch.log(action_prob[action]) * reward  # Assume a simple REINFORCE loss
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch + 1} completed')
    env.render()

env.close()
