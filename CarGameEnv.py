import gymnasium as gym
import numpy as np
from Main import MainGame

class CarGameEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = gym.spaces.Box(low=np.array([0, 0, 0, -180]), high=np.array([800, 600, 10, 180]), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(4)
        self.game_instance = MainGame()

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
        print(f"CarGameEnv --> State: {next_state}, Reward: {reward}, Done: {done}")
        return next_state, reward, done, info

    def _get_state(self):
        car = self.game_instance.car
        return np.array([car.position[0], car.position[1], car.speed, car.wheel_angle]).astype(np.float32)


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
