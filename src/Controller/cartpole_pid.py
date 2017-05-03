import gym
import pid

cont_angle = pid.PID(Kp=5, Ki=0.1, Kd=-0.5)
env = gym.make('CartPole-v0')
env.reset()
env.render()
step = 0

while(True):
    state = env.step(step)
    deviation = - (sum([-0 * state[0][0], 1 * state[0][1], 3 * state[0][2], 1 * state[0][3]]))
    step = cont_angle.step(deviation)
    step = 0 if step > 0 else 1
    if state[2]:
        print('done!')
       #  env.reset()
    env.render()

