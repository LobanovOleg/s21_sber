import yaml

class Dump(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dump, self).increase_indent(flow, False)
    
with open("../materials/todo.yml") as fp:
        todo = yaml.safe_load(fp)

server_packages = todo['server']['install_packages']
exploit_files = todo['server']['exploit_files']
bad_guys = todo['bad_guys']

deploy = {
    'hosts': 'webserver',
    'become': True,
    'tasks': [
                 {
                     'name': 'Install packages',
                     'apt': 'name={pkg} state=present'.format(pkg=pkg)
                 } for pkg in server_packages
             ] + [
                 {
                     'name': 'Copy exploit files',
                     'copy': 'src={file} dest=/Users/lowban/Desktop/Python_Piscine/Python_Bootcamp.Day_03-1/{file} mode=0644'.format(file=file)
                 } for file in exploit_files
             ] + [
                 {
                     'name': 'Run consumer.py on remote server with bad_guys argument',
                     'command': 'python3 /Users/lowban/Desktop/Python_Piscine/Python_Bootcamp.Day_03-1/src/consumer.py -e {bg}'.format(bg=','.join(bad_guys))
                 },
                 {
                     'name': 'Run exploit.py on remote server',
                     'command': 'python3 /Users/lowban/Desktop/Python_Piscine/Python_Bootcamp.Day_03-1/src/exploit.py'
                 }
             ]
}

with open('deploy.yml', 'w') as fp:
     yaml.dump(deploy, fp, Dumper=Dump, default_flow_style=False)