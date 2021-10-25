# -*- coding: utf-8 -*-
from mcdreforged.api.command import *
from mcdreforged.api.decorator.new_thread import new_thread

from simple_test.utils import *


def properties_check(src, config_list):
    try:
        import javaproperties as jp
        with open(properties_path, "rb") as f:
            p_list = jp.load(f)
        if p_list['enable-rcon']:
            src.reply(system_return + tr("rcon_opened"))
        else:
            src.reply(system_return + tr("rcon_closed"))
        src.reply(system_return + tr("server_port", str(p_list['server-port'])))
        src.reply(system_return + tr("mcdr_rcon_port", str(config_list['port'])))
        src.reply(system_return + tr("server_rcon_port", str(p_list['rcon.port'])))
        src.reply(system_return + tr("mcdr_rcon_ip", str(config_list['address'])))
        if config_list['enable']:
            if str(p_list['rcon.port']) == str(config_list['port']):
                src.reply(system_return + tr("rcon_port_same"))
            else:
                error_msg(src, 1)
            if str(p_list['rcon.password']) == config_list['password']:
                src.reply(system_return + tr("rcon_pass_same"))
            else:
                error_msg(src, 2)
    except ModuleNotFoundError:
        error_msg(src, 3)


@new_thread('testing')
def test(src: PlayerCommandSource):
    if src.is_player:
        src.reply(system_return + tr("player", src.player))
    src.reply(system_return + tr("permission_level", permission_level[permission_check(src)]))
    config_list = get_yaml(yml)
    if config_list['enable']:
        src.reply(system_return + tr("mcdr_rcon_enable"))
        if src.get_server().is_rcon_running():
            src.reply(system_return + tr("rcon_running"))
        else:
            src.reply(system_return + tr("rcon_not_running"))
    else:
        src.reply(system_return + tr("mcdr_rcon_disable"))
    if permission_check(src) >= 2:
        properties_check(src, config_list)
    else:
        src.reply(tr("error_permission"))


def register_command(server: PluginServerInterface):
    server.register_command(
        Literal(PREFIX).runs(test)
    )


def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!test', tr("main_msg"))
    register_command(server)
