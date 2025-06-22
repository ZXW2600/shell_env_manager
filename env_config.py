import os


# get the path of the python file
GLOBAL_PATH = os.path.dirname(os.path.realpath(__file__))

GLOBAL_SOURCE_PATH = os.path.join(GLOBAL_PATH, "activate_env.zshrc")

activate_config_flag = os.path.join(GLOBAL_PATH, ".activate_config")
activate_modules_list = os.path.join(GLOBAL_PATH, ".activate_modules")

config_dir = os.path.join(GLOBAL_PATH, "configs")
module_dir = os.path.join(GLOBAL_PATH, "modules")

if not os.path.exists(config_dir):
    os.makedirs(config_dir)
if not os.path.exists(module_dir):
    os.makedirs(module_dir)


def config_path(config_name):
    return os.path.join(config_dir, config_name)


def module_path(module_name):
    return os.path.join(module_dir, module_name)


def get_activated_config():
    config = None
    with open(activate_config_flag, "r") as f:
        config = f.read().strip()
    if config == "":
        return None
    if config is None:
        return None
    if not os.path.exists(config_path(config)):
        print(f"Config {config} does not exist!")
        return None
    return config


def get_activated_modules():
    activated_modules = []
    with open(activate_modules_list, "r") as f:
        for line in f:
            module = line.strip()
            if not os.path.exists(module_path(module)):
                print(f"Module {module} does not exist!")
                continue
            activated_modules.append(module)
    return activated_modules


def get_all_configs():
    return os.listdir(os.path.join(GLOBAL_PATH, "configs"))


def get_all_modules():
    return os.listdir(os.path.join(GLOBAL_PATH, "modules"))


def activate_config(config_name):
    if config_name not in get_all_configs():
        print(f"Config {config_name} does not exist!")
        return
    with open(activate_config_flag, "w") as f:
        f.write(config_name)

    refresh_zshrc()


def activate_module(module_name):
    if module_name not in get_all_modules():
        print(f"Module {module_name} does not exist!")
        return

    if module_name in get_activated_modules():
        print(f"Module {module_name} is already activated!")
        return
    with open(activate_modules_list, "a") as f:
        f.write(module_name + "\n")
    refresh_zshrc()


def deactivate_config():
    with open(activate_config_flag, "w") as f:
        f.write("")
    refresh_zshrc()


def deactivate_module(module_name):
    with open(activate_modules_list, "r") as f:
        lines = f.readlines()
    with open(activate_modules_list, "w") as f:
        for line in lines:
            if line.strip() != module_name:
                f.write(line)
    refresh_zshrc()


def refresh_zshrc():
    activated_config = get_activated_config()
    activated_modules = get_activated_modules()

    config_zsh_rc_path = os.path.join(GLOBAL_PATH, ".activate_config.zshrc")
    modules_zsh_rc_path = os.path.join(GLOBAL_PATH, ".activate_modules.zshrc")

    if activated_config is not None:
        with open(config_zsh_rc_path, "w") as f:
            f.write(f"# {activated_config}\n")
            # f.write(f"source {config_path(activated_config)}\n")
            # export the config_name to the environment variable
            f.write(f"export DEFAULT_ZXW_CONFIG={activated_config}")

    else:
        with open(config_zsh_rc_path, "w") as f:
            f.write("# No config activated\n")

    with open(modules_zsh_rc_path, "w") as f:
        f.write("# modules\n")
        for module in activated_modules:
            f.write(f"source {module_path(module)}\n")


def edit_config(config_name):
    config_file = config_path(config_name)
    os.system(f"vim {config_file}")


def edit_module(module_name):
    module_file = module_path(module_name)
    os.system(f"vim {module_file}")


def create_config(config_name, copy_from):
    if copy_from == "" or copy_from is None:
        os.system(f"touch {config_path(config_name)}")
    else:
        os.system(f"cp {config_path(copy_from)} {config_path(config_name)}")
    edit_config(config_name)


def create_module(module_name, copy_from):
    if copy_from == "" or copy_from is None:
        os.system(f"touch {module_path(module_name)}")
    else:
        os.system(f"cp {module_path(copy_from)} {module_path(module_name)}")
    edit_module(module_name)


def delete_config(config_name):
    if config_name == get_activated_config():
        deactivate_config()
    os.system(f"rm {config_path(config_name)}")


def delete_module(module_name):
    if module_name in get_activated_modules():
        deactivate_module(module_name)
    os.system(f"rm {module_path(module_name)}")


def enter_config(config_name):
    if config_name not in get_all_configs():
        print(f"Config {config_name} does not exist!")
        return
    # start a new shell with the config activated
    command = 'env -i ZXW_CONFIG_NAME=drones HOME="$HOME" USER="$USER" SHELL=/bin/zsh TERM="$TERM" PATH="$PATH" zsh --login'
    os.system(command)
