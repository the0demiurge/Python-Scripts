from app import app
from app import shadowsocks_free_qrcode
from app import ss
from flask import render_template, send_from_directory
import random
import time
import os


servers = shadowsocks_free_qrcode.main()
curtime = time.ctime()

counter_path = os.path.expanduser('~/python/counter')
def counter(counter_path=counter_path):
    if not os.path.exists(os.path.split(counter_path)[0]):
        os.makedirs(os.path.split(counter_path)[0])
    if not os.path.exists(counter_path):
        open(counter_path, 'w').write('0')
    count = int(open(counter_path).readline())
    open(counter_path, 'w').write(str(count + 1))
    return count


def gen_canvas_nest():
    """为背景很绚丽的特效生成随机参数
    """
    color = ','.join([str(random.randint(0, 255)) for i in range(3)])
    opacity = str(random.random()+0.5)
    count = str(random.randint(0, 150))
    return color, opacity, count


@app.route('/')
def index():
    global servers
    servers = shadowsocks_free_qrcode.main()
    color, opacity, count = gen_canvas_nest()
    return render_template(
        'index.html',
        servers=servers,
        ss=ss[random.randint(0, len(ss)-1)],
        counter=counter(),
        color=color,
        opacity=opacity,
        count=count,
        ctime=curtime,
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
    ssr_protocol = servers[ind]['ssr_protocol'] if 'ssr_protocol' in servers[ind] else 'None'
    obfs = servers[ind]['obfs'] if 'obfs' in servers[ind] else 'None'
    href = servers[ind]['href'] if 'href' in servers[ind] else 'None'
    json = servers[ind]['json'] if 'json' in servers[ind] else 'None'
    color, opacity, count = gen_canvas_nest()
    
    return render_template(
        'pages.html',
        uri=uri,
        qrcode=qrcode,
        server=server,
        server_port=server_port,
        password=password,
        method=method,
        ssr_protocol=ssr_protocol,
        obfs=obfs,
        href=href,
        name=name,
        counter=counter(),
        server_data=servers[ind],
        color=color,
        opacity=opacity,
        count=count,
        json=json,
    )


@app.route('/js/<path:path>')
def send_jsadfsadfs(path):
    counter()
    return send_from_directory('js', path)


@app.errorhandler(404)
def page_not_found(e):
    counter()
    color, opacity, count = gen_canvas_nest()
    return render_template(
        '404.html',
        color=color,
        opacity=opacity,
        count=count,
    ), 404
