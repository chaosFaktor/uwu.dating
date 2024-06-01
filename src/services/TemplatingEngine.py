import pystache
import json

renderer = pystache.Renderer(search_dirs=["views/templates", "views/partials"])

def render(asset, bonus_data=False):
    data = json.loads(open(asset, 'r').read())
    if (bonus_data!=False):
        data.update(bonus_data)
    return renderer.render(open(data["template"], 'r').read(), data)
