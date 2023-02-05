import warnings
import json
from bs4 import BeautifulSoup

class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.paths = []
    
    def load_from_svg(self, svg):
        contents = svg
        warnings.simplefilter("ignore")
        soup = BeautifulSoup(contents, 'html.parser')
        svg_el = soup.find('svg')
        self.width = float(svg_el.get('width'))
        self.height = float(svg_el.get('height'))
        
        for el in svg_el.find_all(['path']):
            path_str = el.get('d')
            self.paths.append({
                'id': el.get('id') or None,
                'name': el.get('name') or None,
                'path': path_str,
            })
        
    def get_config(self):
        paths = {}
        for path in self.paths:
            paths[path['id']] = {
                'name': path['name'],
                'path': path['path']
            }
        return {
            'width': self.width,
            'height': self.height,
            'paths': paths
        }
    
    def get_result(self, name):
        map_config = self.get_config()
        stry = f"jQuery.fn.vectorMap('addMap', '{name}', {json.dumps(map_config)});"
        return stry
