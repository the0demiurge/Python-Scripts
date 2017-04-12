import gym
import pid

cont_angle = pid.PID()
env = gym.make('CartPole-v0')
env.reset()
env.render()
step = 0

while(True):
    state = env.step(step)
    step0 = cont_angle.step(state[0][0])
    step1 = cont_angle.step(state[0][1])
    step2 = cont_angle.step(state[0][2])
    step3 = cont_angle.step(state[0][3])
    step = step0 + step1 + step2 + step3
    step = 0 if step > 0 else 1
    if state[2]:
        print('done!')
       #  env.reset()
    env.render()

