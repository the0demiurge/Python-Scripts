from app import app
from flask import render_template
from app import shadowsocks_free_qrcode


servers = shadowsocks_free_qrcode.main()


@app.route('/<int:ind>')
def pages(ind):
    ind -= 1
    uri = servers[ind]['decoded_url'] if 'decoded_url' in servers[ind] else 'None'
    name = servers[ind]['name'] if 'name' in servers[ind] else 'None'
    qrcode = servers[ind]['qrcode'] if 'qrcode' in servers[ind] else 'None'
    server = servers[ind]['server'] if 'server' in servers[ind] else 'None'
    server_port = servers[ind]['server_port'] if 'server_port' in servers[ind] else 'None'
    password = servers[ind]['password'] if 'password' in servers[ind] else 'None'
    method = servers[ind]['method'] if 'method' in servers[ind] else 'None'
    ssr_portal = servers[ind]['ssr_portal'] if 'ssr_portal' in servers[ind] else 'None'
    confuse = servers[ind]['confuse'] if 'confuse' in servers[ind] else 'None'
    href = servers[ind]['href'] if 'href' in servers[ind] else 'None'

    return render_template('pages.html',
                           uri=uri,
                           qrcode=qrcode,
                           server=server,
                           server_port=server_port,
                           password=password,
                           method=method,
                           ssr_portal=ssr_portal,
                           confuse=confuse,
                           href=href,
                           name=name)


@app.route('/')
def index():
    return render_template('index.html', servers=servers)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
