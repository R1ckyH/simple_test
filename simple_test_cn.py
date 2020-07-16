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

error_permission = error + '你没有权限去使用此指令'
error_permission_status = error + '你需要获得§d[helper]§c以上的权限去获取更多资讯§r'

error_rcon_port = error + '''§eserver.properties§r 和 §econfig.yml§r 的 §arcon port§r 不一致
§c为了让服务器得以正常运行， 请修改他们!!!§r'''
error_rcon_password = error + '''§eserver.properties§r 和 §econfig.yml§r 的 §arcon password§r 不一致
§c为了让服务器得以正常运行， 请修改他们!!!§r'''
error_module = system_return + '''安装 §cpython§r 模块 [§ejproperties§r]以获得更多资讯
''' + system_return + '''使用 §7pip install jproperties§r 来为python 安装此模块'''

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
        server.logger.info(system_return + '服务器会在' + str(countdown - i) +  '秒后重启')
        server.say(system_return + '服务器会在' + str(countdown - i) +  '秒后重启')
        time.sleep(1)
    server.restart()


def properties_check(server, info, config_list):
    try:
        from jproperties import Properties
        p_list = Properties()
        with open(properties_path, "rb") as f:
            p_list.load(f)
        server.tell(info.player, system_return + '服务器§e端口§r是§d[' + str(p_list.get('server-port').data) + ']§r')
        server.tell(info.player, system_return + "§eMCDR's§r的§arcon port§r是§d[" + str(config_list['rcon_port']) + ']§r')
        server.tell(info.player, system_return + "§e服务器§r的§arcon port§r是§d[" + str(p_list.get('rcon.port').data) + ']§r')
        if str(p_list.get('rcon.port').data) == str(config_list['rcon_port']):
            server.tell(info.player, system_return + '§aRcon port§b 一致')
        else:
            error_msg(server, info.player, 1)
        if p_list.get('rcon.password').data == config_list['rcon_password']:
            server.tell(info.player, system_return + '§aRcon password§b 一致')
        else:
            error_msg(server, info.player, 2)
    except ModuleNotFoundError:
        error_msg(server, info.player, 3)


def test(server, info):
    server.tell(info.player, system_return + '玩家名 §d' + info.player)
    server.tell(info.player, system_return + '你的§a权限等级§r是§d[' + permission_level[permission_check(server, info)] + ']§r')
    config_list = config.Config(server, constant.CONFIG_FILE)
    config_list.read_config()
    if config_list['enable_rcon']:
        server.tell(info.player, system_return + '服务器的§arcon §r已经§b开启')
        if server.is_rcon_running():
            server.tell(info.player, system_return + '服务器§arcon §r正在§b运行')
        else:
            server.tell(info.player, system_return + '服务器§arcon §c没有运行')
    else:
        server.tell(info.player, system_return + '服务器§arcon §r已经§c关闭§r')
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
    server.add_help_message('!!test','服务器自检插件.')
    server.add_help_message('!!restart','重启服务器.')


def on_info(server, info):
    info2 = copy.deepcopy(info)
    info2.isPlayer = info2.is_player
    onServerInfo(server, info2)