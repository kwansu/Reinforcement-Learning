### DQN Avoid Config ###

env = {
    "name": "avoid2",
    "render": True,
    "screen_width": 300,
    "screen_height": 400,
    "dead_penalty": True,
}

agent = {
    "name": "dqn",
    "network": "dqn",
    "head": "cnn_small",
    "gamma": 0.99,
    "epsilon_init": 1.0,
    "epsilon_min": 0.1,
    "explore_ratio": 0.5,
    "buffer_size": 100000,
    "batch_size": 32,
    "start_train_step": 100000,
    "target_update_period": 10000,
}

optim = {
    "name": "rmsprop",
    "lr": 2.5e-4,
}

train = {
    "training": True,
    "load_path": './logs/avoid2/dqn/20211226041501',
    "run_step": 400000,
    "print_period": 10000,
    "save_period": 100000,
    "eval_iteration": 5,
    "record": True,
    "record_period": 300000,
    # distributed setting
    "update_period": 32,
    "num_workers": 8,
}
