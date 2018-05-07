# coding=utf8
# author:Star
# time:07/05/2018
from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ssh_address_or_host=('yeats.ucd.ie', 22),  # 指定ssh登录的跳转机的address
    ssh_username='xingyu',  # 跳转机的用户
    ssh_password='vKZkv3rt',  # 跳转机的密码
    local_bind_address=('127.0.0.1', 10000),  # 本地绑定的端口
    remote_bind_address=('127.0.0.1', 9609))  # 远程绑定的端口

server.start()