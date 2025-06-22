eval "$(register-python-argcomplete3 ${0:a:h}/env_manager)"

alias env_manager="${0:a:h}/env_manager"
# source .activate_config.zshrc relative to this file
source "${0:a:h}/.activate_modules.zshrc"
source "${0:a:h}/.activate_config.zshrc"

# if ZXW_CONFIG_NAME is set, set to DEFAULT_ZXW_CONFIG
if [[ -n "${ZXW_CONFIG_NAME}" ]]; then
  export DEFAULT_ZXW_CONFIG="${ZXW_CONFIG_NAME}"
fi

# source config 
source "${0:a:h}/configs/${DEFAULT_ZXW_CONFIG}"
