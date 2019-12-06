from gym.envs.registration import register

register(
id='kenage-v0',
entry_point='gym_kenage.envs:KenageEnv',
)
