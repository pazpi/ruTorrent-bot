# handleTorrent
# function to manipulate all the torrent part
def Hash2Magnet(hash):
    magnet = ''
    megnet = "magnet:?xt=urn:btih:" + hash
    return magnet


def addMagnet(torrent):
    torrent = torrent[2:-2]
    url = host + 'ruTorrent/php/addtorrent.php?url=' + torrent
    # Test ArchLinux ISO
    # url = 'http://192.168.1.190/ruTorrent/php/addtorrent.php?url=' + 'magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce'
    requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
