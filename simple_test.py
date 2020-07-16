# -*- coding: utf-8 -*-
import copy
import time
import ruamel.yaml as yaml
from utils import config, constant


plugin = '''simple_test'''
properties_path = '''./server/server.properties'''

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

error_permission = error + 'You have no Permission to use this command'
error_permission_status = error + 'You should have §d[helper]§r§c or higher permission to get more status§r'

error_rcon_port = error + '''§aRcon port§r of §eserver.properties§r is not equal to §econfig.yml
§cPlease correct them to same to ensure server run correctly§r'''
error_rcon_password = error + '''§aRcon password§r of §eserver.properties§r is not equal to §econfig.yml
§cPlease correct them to same to ensure server run correctly§r'''
error_module = system_return + '''Install §cpython§r module §cjproperties§r for more information
''' + system_return + '''Use §7pip install jproperties§r to get the module of python'''

def permission_check(server, info):
    if info.isPlayer:
        return server.get_permission_level(info.player)
    else:
        return 999


def error_msg(server, player, num):
    if num == 0:
        server.tell(player, error_permission)
    elif num == 1:
        server.tell(player, error_rcon_port)
    elif num == 2:
        server.tell(player, error_rcon_password)
    elif num == 3:
        server.tell(player, error_module)

def restart_server(server):
    for i in range(0, countdown):
        server.logger.info(system_return + 'The server will restart after ' + str(countdown - i) +  ' second')
        server.say(system_return + 'The server will restart after ' + str(countdown - i) +  ' second')
        time.sleep(1)
    server.restart()


def properties_check(server, info, config_list):
    try:
        from jproperties import Properties
        p_list = Properties()
        with open(properties_path, "rb") as f:
            p_list.load(f)
        server.tell(info.player, system_return + "§eServer's §aport§r is §d[" + str(p_list.get('server-port').data) + ']§r')
        server.tell(info.player, system_return + "§eMCDR's§r §arcon port§r is §d[" + str(config_list['rcon_port']) + ']§r')
        server.tell(info.player, system_return + "§eServer's§r §arcon port§r is §d[" + str(p_list.get('rcon.port').data) + ']§r')
        if str(p_list.get('rcon.port').data) == str(config_list['rcon_port']):
            server.tell(info.player, system_return + '§aRcon port§r are §bsame')
        else:
            error_msg(server, info.player, 1)
        if p_list.get('rcon.password').data == config_list['rcon_password']:
            server.tell(info.player, system_return + '§aRcon password§r are §bsame')
        else:
            error_msg(server, info.player, 2)
    except ModuleNotFoundError:
        error_msg(server, info.player, 3)


def test(server, info):
    server.tell(info.player, system_return + 'Player §d' + info.player)
    server.tell(info.player, system_return + 'Your §apermission level§r is §d[' + permission_level[permission_check(server, info)] + ']§r')
    config_list = config.Config(server, constant.CONFIG_FILE)
    config_list.read_config()
    if config_list['enable_rcon']:
        server.tell(info.player, system_return + "§eMCDR's §arcon§r are §benabled")
        if server.is_rcon_running():
            server.tell(info.player, system_return + "§eServer's §arcon§r is §brunning")
        else:
            server.tell(info.player, system_return + "§eServer's §arcon§r is§c not running")
    else:
        server.tell(info.player, system_return + "§eMCDR's §arcon§r are §cdisabled§r")
    if permission_check(server, info) >= 2:
        properties_check(server, info, config_list)
    else:
        server.tell(info.player, error_permission_status)


def onServerInfo(server, info):
    if info.content.startswith('!!restart'):
        if permission_check(server, info) > 2:
            restart_server(server)
        else:
            error_msg(server, info.player, 0)
    elif info.content.startswith('!!test') and info.isPlayer:
        test(server, info)


def on_load(server, old):
    server.add_help_message('!!test','testing server problem.')
    server.add_help_message('!!restart','restart server.')


def on_info(server, info):
    info2 = copy.deepcopy(info)
    info2.isPlayer = info2.is_player
    onServerInfo(server, info2)