PREFIX = '!!test'
plugin = '''simple_test'''
properties_path = '''./server/server.properties'''
yml = 'config.yml'

countdown = 10
permission_level = {
    0: "guest",
    1: "user",
    2: "helper",
    3: "admin",
    4: "owner",
    999: "server"
}


system_return = f'''§b[§r{plugin}§b] §r'''
error = system_return + '''§cError: '''
