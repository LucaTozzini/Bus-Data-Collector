import os


def getQuery(path):
    if '?' not in path:
        return {}
    
    url_request = path.split('?')[1]
    dict = {}
    for q in url_request.split('&'):
        key_val = q.split('=') 
        dict[key_val[0]] = key_val[1]
    return dict

def getParams(template, path):
    dict = {}
    if template.endswith('/'):
        template = template[:-1]
    if path.endswith('/'):
        path = path[:-1]
    if len(path.split('/')) != len(template.split('/')):
        return 'mismatch' 
    if ':' in template:
        index = 0
        for section in template.split('/'):
            if ':' in section:
                dict[section.split(':')[1]] = path.split('/')[index].split('?')[0]
            index+=1
    return dict
        
def staticFolder(path, self):
    if self.path.startswith('/'):
        if not os.path.exists(path+self.path) or '..' in self.path:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        with open(path+self.path, 'rb') as file:
            response = file.read()
            self.wfile.write(response)