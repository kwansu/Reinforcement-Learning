### DQN Avoid Config ###

env = {
    "name": "othello",
    "render": True,
    "screen_width": 400,
    "screen_height": 400,
}

agent = {
    "name": "dqn_othello",
    "head": "cnn_othello",
    "hidden_size": 512,
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
    "load_path": None,#'./logs/othello/dqn/20211229090750',
    "run_step": 1000000,
    "print_period": 10000,
    "save_period": 100000,
    "eval_iteration": 5,
    "record": True,
    "record_period": 300000,
    # distributed setting
    "update_period": 32,
    "num_workers": 8,
}
