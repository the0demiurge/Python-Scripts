import gym
import pid
import numpy as np
import multiprocessing
from matplotlib import pyplot


def run(Kp=5, Ki=.1, Kd=.1, rho=0.5, n_iter=900, close=True, params=[0, -1, -1, -1]):
    # This runs one iterate with given parameters
    # INIT
    controller = pid.PID(Kp=Kp, Ki=Ki, Kd=Kd)
    us = list()
    es = list()
    env = gym.make('CartPole-v0')
    env.reset()
    env.render(close=close)

    def decide_step(u):
        # Because there are only 2 steps, simply discretization the step.
        if u > 0:
            return 1
        elif u < 0:
            return 0
        else:
            return np.random.randint(0, 2)

    # There are only 2 steps, `0, 1`. Choose first step randomly
    step = decide_step(0)

    for i in range(n_iter):
        # Add interferce at timestamp 20
        if i == 20:
            for i in range(4):
                env.step(0)
        if i == 60:
            for i in range(4):
                env.step(1)
        state = env.step(step)
        # The giver amount is all-zero, consequently the deviation is -(sum(...))
        e = - (sum(map(lambda x: x[0] * x[1], zip(params, state[0]))))
        # Get the control amount
        u = controller.step(e)
        step = decide_step(u)
        us.append(u)
        es.append(e)
        env.render(close=close)

    loss = sum(map(lambda x: x ** 2, us)) + rho * sum(map(lambda x: x ** 2, es))
    return loss, us, es


def cem(func, mean, variance, n=100, ratio=.2, max_iter=1000, min_var=0.001):
    """Cross-Entropy Method Optimizer, using Gaussian distribution approximation. Minimize loss returned from func
    Args:
        func receives parameters and returns loss only
        mean and variance: mean and variance of the init gaussian
        n: size of tries per iterate
        ratio: re-sampling referance ratio
        max_iter, min_var: stop condition

    Returns:
        param: best parameters
        mean: mean of parameters
        variance: variance of parameters
        traj: min-loss curve durning optimizing
    """

    # Check input
    n_ref = int(n * ratio)
    n_params = len(tuple(zip(mean, variance)))
    traj = list()
    assert n > 0, 'n not > 0'
    assert 0 < n_ref < n, 'n_ref out-bounded'
    assert min_var > 0, 'min_var not > 0'
    assert min(variance) > 0, 'variance not > 0'

    pool = multiprocessing.Pool()
    for _ in range(max_iter):
        params = np.random.randn(n, n_params)
        for i, p in enumerate(zip(mean, variance)):
            params[:, i] = params[:, i] * np.sqrt(p[1]) + p[0]
        loss = pool.map(func, params)
        sorted_params, sorted_loss = zip(*sorted(zip(params, loss), key=lambda x: x[-1]))
        traj.append(sorted_loss[0])
        params_ref = np.array(sorted_params[:n_ref])
        mean = np.mean(params_ref, axis=0)
        variance = np.var(params_ref, axis=0)
        if min(variance) < min_var:
            break
    return list(params_ref[0]), mean, variance, traj


def run_(x, rho=.5, close=True):
    # This function is designed for multi-subprocess
    return run(x[0], x[1], x[2], close=close, rho=rho)[0]


def run0(x):
    return run_(x, rho=0)


def run_25(x):
    return run_(x, rho=.25)


def run_5(x):
    return run_(x, rho=.5)


def run_75(x):
    return run_(x, rho=.75)


def run1(x):
    return run_(x, rho=1)


def main():
    data = dict()
    for func, rho in zip([run0, run_25, run_5, run_75, run1], [0, .25, 0.5, .75, 1]):
        best, mean, variance, traj = cem(func, [10, 0, 0], [60, 40, 40])
        loss, us, es = run(mean[0], mean[1], mean[2], rho, n_iter=500, close=False)
        data[rho] = {
            'traj': traj,
            'us': us,
            'es': es,
            'best': best,
            'mean': mean,
            'variance': variance,
        }

    # Print information
    for rho in data:
        print('''rho = {}
              Best params: {}
              Mean of params: {}
              Var of params: {}
              Var of u: {}
              Mean of u: {}
              Var of e: {}
              Mean of e: {}
              \n'''.format(
            rho,
            data[rho]['best'],
            data[rho]['mean'],
            data[rho]['variance'],
            np.var(data[rho]['us']),
            np.mean(data[rho]['us']),
            np.var(data[rho]['es']),
            np.mean(data[rho]['es']),
        ))

    # Plot optimizion trajectory
    pyplot.figure()
    for rho in data:
        pyplot.plot(data[rho]['traj'], '*-', label='$\\rho={}$'.format(rho))
    pyplot.xlabel('Optimizing Iteration')
    pyplot.ylabel('Min Loss')
    pyplot.legend()

    # Plot us
    pyplot.figure()
    for rho in data:
        plot_data = data[rho]['us']
        # moving_average = list(map(lambda x: x[-1] / 2 + x[-2] / 4 + (x[-3] + x[-4]) / 8, zip(plot_data, plot_data[1:], plot_data[2:], plot_data[3:])))
        pyplot.plot(plot_data[:100], label='$\\rho={}$'.format(rho))
    pyplot.xlabel('$t$')
    pyplot.ylabel('Input amount')
    pyplot.legend()

    # Plot es
    pyplot.figure()
    for rho in data:
        plot_data = data[rho]['es']
        # moving_average = list(map(lambda x: x[-1] / 2 + x[-2] / 4 + (x[-3] + x[-4]) / 8, zip(plot_data, plot_data[1:], plot_data[2:], plot_data[3:])))
        pyplot.plot(plot_data[:100], label='$\\rho={}$'.format(rho))
    pyplot.xlabel('$t$')
    pyplot.ylabel('Deviation')
    pyplot.legend()
    pyplot.show()


if __name__ == '__main__':
    main()
