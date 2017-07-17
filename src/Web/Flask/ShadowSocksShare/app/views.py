from app import app
from flask import render_template, send_from_directory
from app import shadowsocks_free_qrcode
import random

ss = ['''
  mmmm  #                 #                 mmmm                #
 #"   " # mm    mmm    mmm#   mmm  m     m #"   "  mmm    mmm   #   m   mmm
 "#mmm  #"  #  "   #  #" "#  #" "# "m m m" "#mmm  #" "#  #"  "  # m"   #   "
     "# #   #  m"""#  #   #  #   #  #m#m#      "# #   #  #      #"#     """m
 "mmm#" #   #  "mm"#  "#m##  "#m#"   # #   "mmm#" "#m#"  "#mm"  #  "m  "mmm"

                                                                             ''',
      ''' ____  _               _                ____             _
/ ___|| |__   __ _  __| | _____      __/ ___|  ___   ___| | _____
\___ \| '_ \ / _` |/ _` |/ _ \ \ /\ / /\___ \ / _ \ / __| |/ / __|
 ___) | | | | (_| | (_| | (_) \ V  V /  ___) | (_) | (__|   <\__ \\
|____/|_| |_|\__,_|\__,_|\___/ \_/\_/  |____/ \___/ \___|_|\_\___/


''']


servers = shadowsocks_free_qrcode.main()
counter = 0


def gen_canvas_nest():
    """为背景很绚丽的特效生成随机参数
    """
    color = ','.join([str(random.randint(0, 255)) for i in range(3)])
    opacity = str(random.random()+0.5)
    count = str(random.randint(0, 500))
    return color, opacity, count


@app.route('/')
def index():
    global counter
    counter += 1
    color, opacity, count = gen_canvas_nest()
    return render_template(
        'index.html',
        servers=servers,
        ss=ss[random.randint(0, 1)],
        counter=counter,
        color=color,
        opacity=opacity,
        count=count,
    )


@app.route('/<int:ind>')
def pages(ind):
    ind -= 1
    uri = servers[ind]['decoded_url'] if 'decoded_url' in servers[ind] else ''
    name = servers[ind]['name'] if 'name' in servers[ind] else 'None'
    qrcode = servers[ind]['qrcode'] if 'qrcode' in servers[ind] else ''
    server = servers[ind]['server'] if 'server' in servers[ind] else 'None'
    server_port = servers[ind]['server_port'] if 'server_port' in servers[ind] else 'None'
    password = servers[ind]['password'] if 'password' in servers[ind] else 'None'
    method = servers[ind]['method'] if 'method' in servers[ind] else 'None'
    ssr_portal = servers[ind]['ssr_portal'] if 'ssr_portal' in servers[ind] else 'None'
    confuse = servers[ind]['confuse'] if 'confuse' in servers[ind] else 'None'
    href = servers[ind]['href'] if 'href' in servers[ind] else 'None'
    global counter
    counter += 1
    color, opacity, count = gen_canvas_nest()

    return render_template(
        'pages.html',
        uri=uri,
        qrcode=qrcode,
        server=server,
        server_port=server_port,
        password=password,
        method=method,
        ssr_portal=ssr_portal,
        confuse=confuse,
        href=href,
        name=name,
        counter=counter,
        server_data=servers[ind],
        color=color,
        opacity=opacity,
        count=count,
    )


@app.route('/js/<path:path>')
def send_jsadfsadfs(path):
    return send_from_directory('js', path)


@app.errorhandler(404)
def page_not_found(e):
    global counter
    counter += 1
    color, opacity, count = gen_canvas_nest()
    return render_template(
        '404.html',
        color=color,
        opacity=opacity,
        count=count,
    ), 404
