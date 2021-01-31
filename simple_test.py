# -*- coding: utf-8 -*-
import ruamel.yaml as yaml
from mcdreforged.api.types import *
from mcdreforged.api.command import *
from mcdreforged.api.rtext import *


PLUGIN_METADATA = {
    'id': 'simple_test',
    'version': '2.1.2',
    'name': 'simple_test',
    'description': 'testing server problem.',
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

error_permission_status = error + 'You should have §d[helper]§r§c or higher permission to get more status§r'
error_rcon_port = error + '''§aRcon port§r of §eserver.properties§r is not equal to §econfig.yml
§cPlease correct them to same to ensure server run correctly§r'''
error_rcon_password = error + '''§aRcon password§r of §eserver.properties§r is not equal to §econfig.yml
§cPlease correct them to same to ensure server run correctly§r'''
error_module = system_return + '''Install §cpython§r module §cjproperties§r for more information
''' + system_return + '''Use §7pip install jproperties§r to get the module of python'''

def get_ymal():
    with open(yml, 'r') as y:
        content = yaml.load(y, Loader = yaml.Loader)
        print(content['rcon'])
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
        from jproperties import Properties
        p_list = Properties()
        with open(properties_path, "rb") as f:
            p_list.load(f, encoding = 'utf-8')
        if p_list.get('enable-rcon').data:
            src.reply(system_return + '''§eServer's§arcon §ris §bopened''')
        else:
            src.reply(system_return + '''§eServer's§arcon §ris §bclosed''')
        src.reply(system_return + "§eServer's §aport§r is §d[" + str(p_list.get('server-port').data) + ']§r')
        src.reply(system_return + "§eMCDR's§r §arcon port§r is §d[" + str(config_list['port']) + ']§r')
        src.reply(system_return + "§eServer's§r §arcon port§r is §d[" + str(p_list.get('rcon.port').data) + ']§r')
        src.reply(system_return + "§eMCDR's §r§arcon ip is §d[" + str(config_list['address']) + ']§r')
        if config_list['enable']:
            if str(p_list.get('rcon.port').data) == str(config_list['port']):
                src.reply(system_return + '§aRcon port§r are §bsame')
            else:
                error_msg(src, 1)
            if p_list.get('rcon.password').data == config_list['password']:
                src.reply(system_return + '§aRcon password§r are §bsame')
            else:
                error_msg(src, 2)
    except ModuleNotFoundError:
        error_msg(src, 3)


def test(src : CommandSource):
    if src.is_player:
        src.reply(system_return + 'Player §d' + src.player)
    src.reply(system_return + 'Your §apermission level§r is §d[' + permission_level[permission_check(src)] + ']§r')
    config_list = get_ymal()
    if config_list['enable']:
        if src.get_server().is_rcon_running():
            src.reply(system_return + "§eServer's §arcon§r is §brunning")
        else:
            src.reply(system_return + "§eServer's §arcon§r is§c not running")
        src.reply(system_return + "§eMCDR's §arcon§r are §benabled")
    else:
        src.reply(system_return + "§eMCDR's §arcon§r are §cdisabled§r")
    if permission_check(src) >= 2:
        properties_check(src, config_list)
    else:
        src.reply(error_permission_status)


def register_command(server : ServerInterface):
    server.register_command(
        Literal(prefix).
        runs(test)
    )


def on_load(server : ServerInterface, old):
    server.register_help_message('!!test','testing server problem.')
    register_command(server)