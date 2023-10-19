import gymnasium as gym
import numpy as np
from Main import MainGame
from pygame import surfarray

class CarGameEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(4)
        self.game_instance = MainGame()
        self.observation_space = gym.spaces.Box(low=0, high=255,
                                                shape=(self.game_instance.screen_height, self.game_instance.screen_width, 3),
                                                dtype=np.uint8)

    def reset(self, seed=None, options=None):
        self.game_instance = MainGame()
        obs = self._get_state()
        info = {}
        return obs, info

    def step(self, action):
        if action == 0:
            self.game_instance.car.accelerate()
        elif action == 1:
            self.game_instance.car.brake_or_drift()
        elif action == 2:
            self.game_instance.car.steer_left()
        elif action == 3:
            self.game_instance.car.steer_right()
            
        self.game_instance.update()
        next_state = self._get_state()
        reward = self._get_reward()
        done = self._is_done()
        info = {}
        # print(f"CarGameEnv --> Reward: {reward}, Done: {done}")
        truncated = False
        return next_state, reward, done, truncated, info

    def _get_state(self):
        screen = surfarray.array3d(self.game_instance.screen)
        # print(f"CarGameEnv --> Screen shape: {screen.shape}")
        return screen.reshape(self.observation_space.shape)

    def _get_reward(self):
        return self.game_instance.getStepScore()

    def _is_done(self):
        if self.game_instance.running == False:
            return True
        return False

    def render(self):
        self.game_instance.render()

    def close(self):
        pass
