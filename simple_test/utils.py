import ruamel.yaml as yaml

from mcdreforged.api.rtext import *
from mcdreforged.api.types import *

from simple_test.resources import *


def tr(key, *args) -> str:
    return ServerInterface.get_instance().tr(f"{plugin}.{key}", *args)


def error_msg(src, num):
    if num == 1:
        src.reply(error + tr("error_permission"))
    elif num == 2:
        src.reply(error + tr("rcon_password"))
    elif num == 3:
        src.reply(error + tr("error_module", system_return,
                             RText('''§7pip install javaproperties§r''').h(f"{tr('click_msg') + tr('to_clipboard')}").c(
                                 RAction.copy_to_clipboard, 'pip install javaproperties')))


def get_yaml(yml_path):
    with open(yml_path, 'r') as y:
        content = yaml.load(y, Loader=yaml.Loader)
        return content['rcon']


def permission_check(src):
    if src.is_player:
        return src.get_permission_level()
    else:
        return 999
