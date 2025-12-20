from setuptools import find_packages,setup
from typing import List
var='-e.'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements'''
    requirments=[]
    with open(file_path) as file_obj:
        requirments=file_obj.readlines()
        requirments=[i.replace('\n','') for i in requirments]
        if var in requirments:
            requirments.remove(var)
    return requirments    

setup(
    name='mlproject',
    version='0.0.1',
    author='vardhan',
    author_email='koradavardhan24@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt'),
)