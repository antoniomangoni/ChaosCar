import torch
import gymnasium as gym

class CarNN(torch.nn.Module):
    def __init__(self, state_dim, action_dim):
        super(CarNN, self).__init__()
        self.layer1 = torch.nn.Linear(state_dim, 128)
        self.layer2 = torch.nn.Linear(128, 64)
        self.layer3 = torch.nn.Linear(64, action_dim)
        
    def forward(self, state):
        output = torch.relu(self.layer1(state))
        output = torch.relu(self.layer2(output))
        output = self.layer3(output)
        return output