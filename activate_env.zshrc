eval "$(register-python-argcomplete3 ${0:a:h}/env_manager)"

alias env_manager="${0:a:h}/env_manager"
# source .activate_config.zshrc relative to this file
source "${0:a:h}/.activate_modules.zshrc"
source "${0:a:h}/.activate_config.zshrc"
