# -*- coding: utf-8 -*-
import ruamel.yaml as yaml
from mcdreforged.api.types import *
from mcdreforged.api.command import *
from mcdreforged.api.rtext import *


PLUGIN_METADATA = {
    'id': 'simple_test',
    'version': '2.1.2-cn',
    'name': 'simple_test_cn',
    'description': '服务器温度警报插件.',
    'author': 'ricky',
    'link': 'https://github.com/rickyhoho/simple_test',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}


prefix = '!!test'
plugin = '''simple_test'''
properties_path = '''./server/server.properties'''
yml = 'config.yml'


countdown = 10
permission_level = {
    0 : "guest",
    1 : "user",
    2 : "helper",
    3 : "admin",
    4 : "owner",
    999 : "server"
}


system_return = '''§b[§rsimple_test§b] §r'''
error = system_return + '''§cError: '''

error_permission_status = error + '你需要获得§d[admin]§c以上的权限去获取更多资讯§r'
error_rcon_port = error + '''§eserver.properties§r 和 §econfig.yml§r 的 §arcon port§r 不一致
§c为了让服务器得以正常运行， 请修改他们!!!§r'''
error_rcon_password = error + '''§eserver.properties§r 和 §econfig.yml§r 的 §arcon password§r 不一致
§c为了让服务器得以正常运行， 请修改他们!!!§r'''
error_module = system_return + '''安装 §cpython§r 模块 [§ejavaproperties§r]以获得更多资讯
''' + system_return + '''使用'''+ RText('''§7pip install javaproperties§r''').h('点击我复制到剪贴板').c(RAction.copy_to_clipboard, 'pip install javaproperties') +''' 来为python 安装此模块'''

def get_ymal():
    with open(yml, 'r') as y:
        content = yaml.load(y, Loader = yaml.Loader)
        return content['rcon']


def permission_check(src):
    if src.is_player:
        return src.get_permission_level()
    else:
        return 999


def error_msg(src, num):
    if num == 1:
        src.reply(error_rcon_port)
    elif num == 2:
        src.reply(error_rcon_password)
    elif num == 3:
        src.reply(error_module)


def properties_check(src, config_list):
    try:
        import javaproperties as jp
        with open(properties_path, "rb") as f:
            p_list = jp.load(f)
        if p_list['enable-rcon']:
            src.reply(system_return + '§e服务器的§arcon §r已经§b开启')
        else:
            src.reply(system_return + '§e服务器§arcon §r已经§c关闭§r')
        src.reply(system_return + '§e服务器§e端口§r是§d[' + str(p_list['server-port']) + ']§r')
        src.reply(system_return + "§eMCDR§r的§arcon port§r是§d[" + str(config_list['port']) + ']§r')
        src.reply(system_return + "§e服务器§r的§arcon port§r是§d[" + str(p_list['rcon.port']) + ']§r')
        src.reply(system_return + "§eMCDR§r的§arcon ip§r是§d[" + str(config_list['address']) + ']§r')
        if config_list['enable']:
            if str(p_list['rcon.port']) == str(config_list['port']):
                src.reply(system_return + '§aRcon port§b 一致')
            else:
                error_msg(src, 1)
            if str(p_list['rcon.password']) == config_list['password']:
                src.reply(system_return + '§aRcon password§b 一致')
            else:
                error_msg(src, 2)
    except ModuleNotFoundError:
        error_msg(src, 3)


def test(src : CommandSource):
    if src.is_player:
        src.reply(system_return + '玩家名 §d' + src.player)
    src.reply(system_return + '你的§a权限等级§r是§d[' + permission_level[permission_check(src)] + ']§r')
    config_list = get_ymal()
    if config_list['enable']:
        if src.get_server().is_rcon_running():
            src.reply(system_return + '§e服务器§arcon §r正在§b运行')
        else:
            src.reply(system_return + '§e服务器§arcon §c没有运行')
        src.reply(system_return + '§eMCDR的§arcon §r已经§b开启')
    else:
        src.reply(system_return + '§eMCDR§arcon §r已经§c关闭§r')
    if permission_check(src) > 2:
        properties_check(src, config_list)
    else:
        src.reply(error_permission_status)


def register_command(server : ServerInterface):
    server.register_command(
        Literal(prefix).
        runs(test)
    )


def on_load(server : ServerInterface, old):
    server.register_help_message('!!test','服务器自检插件.')
    register_command(server)