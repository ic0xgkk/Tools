import os

ip = [
    '10.0.78.11',
    '10.0.78.10',
    '10.0.78.8',
    '10.0.78.7',
    '10.0.78.6',
    '10.0.78.5',
    '10.0.78.4',
    '10.0.78.3',
    '10.0.78.2',
    '10.0.78.102',
    '10.0.78.103',
    '10.0.78.104',
    '10.0.78.105',
    '10.0.78.106',
    '10.0.78.107',
    '10.0.78.108',
    '10.0.78.109',
    '10.0.78.111',
    '10.0.78.112',
    '10.0.78.113',
    '10.0.78.114',
    '10.0.78.116',
    '10.0.78.117',
    '10.0.78.118',
    '10.0.78.119',
    '10.0.78.12',
    '10.0.78.120',
    '10.0.78.121',
    '10.0.78.122',
    '10.0.78.123',
    '10.0.78.124',
    '10.0.78.125',
    '10.0.78.126',
    '10.0.78.127',
    '10.0.78.128',
    '10.0.78.129',
    '10.0.78.13',
    '10.0.78.130',
    '10.0.78.131',
    '10.0.78.132',
    '10.0.78.133',
    '10.0.78.134',
    '10.0.78.135',
    '10.0.78.136',
    '10.0.78.137',
    '10.0.78.14',
    '10.0.78.141',
    '10.0.78.142',
    '10.0.78.143',
    '10.0.78.157',
    '10.0.78.158',
    '10.0.78.159',
    '10.0.78.16',
    '10.0.78.160'
    ]
time = 2
mac_prefix = '90:e7:10:b8:16:'
mac_suffix = 11
text = ''

template = 'id=%s comment= interface=wan1 enabled=yes vlan_id=%s vlan_name=vwan_bl%s mac=%s ' \
           'vlan_internet=0 upload=0 download=0 qos_upload=0 qos_download=0 ip_mask=%s/255.255.255.0' \
           ' gateway=10.0.78.1 username= passwd= timing_rst_switch=0 timing_rst_week=1234567 timing_rst_time=12:00' \
           ' cycle_rst_time=0 pppoe_service= mtu=1480 mru=1480 default_route=0 disc_auto_switch=1 ' \
           'link_time=00:00-23:59 check_link_mode=3 check_link_host=www.taobao.com qos_switch=0'

for i in ip:
    text += template % (str(time), str(time), str(time), mac_prefix + str(mac_suffix), i)
    time += 1
    mac_suffix += 1
    text += '\n'

with open('config.txt', 'w', encoding='utf-8') as f:
    f.write(text)
    f.close()

