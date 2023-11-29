'''
A view module to render html output
'''

from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('5_data-storage/templates')
env = Environment(loader=file_loader)
template = env.get_template('message.html')

def render(name: str, greet: bool, number: int) -> str:
    '''
    Render the template based on the input
    '''
    return template.render(name=name, greet=greet, number=number)
