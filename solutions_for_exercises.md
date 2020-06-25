### 1: Handling Errors When Files Don'T Exist

```python
#!/usr/bin/env python3.6

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file_name', help='the file to read')
parser.add_argument('line_number', type=int, help='the line to print from the file')

args = parser.parse_args()

try:
    lines = open(args.file_name, 'r').readlines()
    line = lines[args.line_number - 1]
except IndexError:
    print(f"Error: file '{args.file_name}' doesn't have {args.line_number} lines.")
except IOError as err:
    print(f"Error: {err}")
else:
    print(line)
```

# ------------------------------------------------------------------------------------------------

# 2: Interacting With External Commands

```python
#!/usr/bin/env python3.6

import subprocess
import os
from argparse import ArgumentParser

parser = ArgumentParser(description='kill the running process listening on a given port')
parser.add_argument('port', type=int, help='the port number to search for')

port = parser.parse_args().port

try:
    result = subprocess.run(
            ['lsof', '-n', "-i4TCP:%s" % port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print(f"No process listening on port {port}")
else:
    listening = None

    for line in result.stdout.splitlines():
        if "LISTEN" in str(line):
            listening = line
            break

    if listening:
        # PID is the second column in the output
        pid = int(listening.split()[1])
        os.kill(pid, 9)
        print(f"Killed process {pid}")
    else:
        print(f"No process listening on port {port}")
```

------------------------------------------------------------------------------------------------

# 3: Setting Exit Status On Errors

```python
#!/usr/bin/env python3.6

import subprocess
import os
from argparse import ArgumentParser
from sys import exit

parser = ArgumentParser(description='kill the running process listening on a given port')
parser.add_argument('port', type=int, help='the port number to search for')

port = parser.parse_args().port

try:
    result = subprocess.run(
            ['lsof', '-n', "-i4TCP:%s" % port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print(f"No process listening on port {port}")
    exit(1)
else:
    listening = None

    for line in result.stdout.splitlines():
        if "LISTEN" in str(line):
            listening = line
            break

    if listening:
        # PID is the second column in the output
        pid = int(listening.split()[1])
        os.kill(pid, 9)
        print(f"Killed process {pid}")
    else:
        print(f"No process listening on port {port}")
        exit(1)
```

------------------------------------------------------------------------------------------------

# 4: Utilizing Third-Party Packages

```python

#!/usr/bin/env python3.6

import sys
import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', help='URL to store the contents of')
parser.add_argument('filename', help='the filename to store the content under')
parser.add_argument('--content-type', '-c',
                    default='html',
                    choices=['html', 'json'],
                    help='the content-type of the URL being requested')

args = parser.parse_args()

res = requests.get(args.url)

if res.status_code >= 400:
    print(f"Error code received: {res.status_code}")
    sys.exit(1)

if args.content_type == 'json':
    try:
        content = json.dumps(res.json())
    except ValueError:
        print("Error: Content is not JSON")
        sys.exit(1)
else:
    content = res.text

with open(args.filename, 'w', encoding='UTF-8') as f:
    f.write(content)
    print(f"Content written to '{args.filename}'")
```

------------------------------------------------------------------------------------------------

# 5. Creating a Python Project

There's more than one way to set up a project, but here's one way that you could. First, set up the project's folder structure:

```
$ mkdir hr
$ cd hr
$ mkdir -p src/hr tests
$ touch src/hr/__init__.py tests/.keep README.rst
```

With the folders setup, you can then utilize `pipenv` to add dependency management:

*Note:* Ensure that `which` has been installed and is in your `$PATH`

```
$ pipenv --python python3.6 install --dev pytest pytest-mock
```

Here's a good starting point for a `setup.py`:

*setup.py*

```
from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='hr',
    version='0.1.0',
    description='Commandline user management utility',
    long_description=readme,
    author='Your Name',
    author_email='person@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[]
)
```

Lastly, initialize the git repository:

```
$ git init
$ curl https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -o .gitignore
$ git add --all .
$ git commit -m 'Initial commit.'
```

------------------------------------------------------------------------------------------------

# 6: Test Drive Building A Cli Parser

Here are some example tests:

*test/test_cli.py*

```python
import pytest

from hr import cli

@pytest.fixture()
def parser():
    return cli.create_parser()

def test_parser_fails_without_arguments(parser):
    """
    Without a path, the parser should exit with an error.
    """
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_parser_succeeds_with_a_path(parser):
    """
    With a path, the parser should exit with an error.
    """
    args = parser.parse_args(['/some/path'])
    assert args.path == '/some/path'

def test_parser_export_flag(parser):
    """
    The `export` value should default to False, but set
    to True when passed to the parser.
    """
    args = parser.parse_args(['/some/path'])
    assert args.export == False

    args = parser.parse_args(['--export', '/some/path'])
    assert args.export == True
```

Here's an example implementation for this `cli` module:

*src/hr/cli.py*

```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to the inventory file (JSON)')
    parser.add_argument('--export', action='store_true', help='export current settings to inventory file')
    return parser
```

------------------------------------------------------------------------------------------------

# 7: Implementing User Management

*tests/test_users.py*

```python
import pytest
import subprocess

from hr import users

# encrypted version of 'password'
password = '$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/'

user_dict = {
    'name': 'kevin',
    'groups': ['wheel', 'dev'],
    'password': password
}

def test_users_add(mocker):
    """
    Given a user dictionary. `users.add(...)` should
    utilize `useradd` to create a user with the password
    and groups.
    """
    mocker.patch('subprocess.call')
    users.add(user_dict)
    subprocess.call.assert_called_with([
        'useradd',
        '-p',
        password,
        '-G',
        'wheel,dev',
        'kevin',
    ])

def test_users_remove(mocker):
    """
    Given a user dictionary, `users.remove(...)` should
    utilize `userdel` to delete the user.
    """
    mocker.patch('subprocess.call')
    users.remove(user_dict)
    subprocess.call.assert_called_with([
        'userdel',
        '-r',
        'kevin',
    ])

def test_users_update(mocker):
    """
    Given a user dictionary, `users.update(...)` should
    utilize `usermod` to set the groups and password for the
    user.
    """
    mocker.patch('subprocess.call')
    users.update(user_dict)
    subprocess.call.assert_called_with([
        'usermod',
        '-p',
        password,
        '-G',
        'wheel,dev',
        'kevin',
    ])

def test_users_sync(mocker):
    """
    Given a list of user dictionaries, `users.sync(...)` should
    create missing users, remove extra non-system users, and update
    existing users. A list of existing usernames can be passed in
    or default users will be used.
    """
    existing_user_names = ['kevin', 'bob']
    users_info = [
        user_dict,
        {
            'name': 'jose',
            'groups': ['wheel'],
            'password': password
        }
    ]
    mocker.patch('subprocess.call')
    users.sync(users_info, existing_user_names)

    subprocess.call.assert_has_calls([
        mocker.call([
            'usermod',
            '-p',
            password,
            '-G',
            'wheel,dev',
            'kevin',
        ]),
        mocker.call([
            'useradd',
            '-p',
            password,
            '-G',
            'wheel',
            'jose',
        ]),
        mocker.call([
            'userdel',
            '-r',
            'bob',
        ]),
    ])
```


Notice about above: Since there were multiple calls made to `subprocess.call` within the `sync` test
we used a different assertion method called `assert_has_calls` which takes a list of `mocker.call` objects.
The `mocker.call` method wraps the content we would otherwise have put in an `assert_called_with` assertion.


*src/hr/users.py*

```python
import pwd
import subprocess
import sys

def add(user_info):
    print(f"Adding user '{user_info['name']}'")
    try:
        subprocess.call([
            'useradd',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print(f"Failed to add user '{user_info['name']}'")
        sys.exit(1)

def remove(user_info):
    print(f"Removing user '{user_info['name']}'")
    try:
        subprocess.call([
            'userdel',
            '-r',
            user_info['name']
        ])
    except:
        print(f"Failed to remove user '{user_info['name']}'")
        sys.exit(1)

def update(user_info):
    print(f"Updating user '{user_info['name']}'")
    try:
        subprocess.call([
            'usermod',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print(f"Failed to update user '{user_info['name']}'")
        sys.exit(1)

def sync(users, existing_user_names=None):
    existing_user_names = (existing_user_names or _user_names())
    user_names = [user['name'] for user in users]
    for user in users:
        if user['name'] not in existing_user_names:
            add(user)
        elif user['name'] in existing_user_names:
            update(user)
    for user_name in existing_user_names:
        if not user_name in user_names:
            remove({ 'name': user_name })

def _groups_str(user_info):
    return ','.join(user_info['groups'] or [])

def _user_names():
    return [user.pw_name for user in pwd.getpwall()
            if user.pw_uid >= 1000 and 'home' in user.pw_dir]

```

I utilized the `pwd` module to get a list of all of the users on the system and determined which ones weren’t system users by looking for UIDs over 999 and ensuring that the user’s directory was under `home`. Additionally, the `join` method on `str` was used to combine a list of values into a single string separated by commas. This action is roughly equivalent to:

```python
index = 0
group_str = ""
for group in groups:
    if index == 0:
        group_str += group
    else:
        group_str += ",%s" % group
    index+=1
```

To manually test this you’ll need to (temporarily) run the following from within your project’s directory:

```
sudo pip3.6 install -e .
```

Then you will be able to run the following to be able to use your module in a REPL without getting permissions errors for calling out to `usermod`, `userdel`, and `useradd`:

```python
sudo python3.6
>>> from hr import users
>>> password = '$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/'
>>> user_dict = {
...     'name': 'kevin',
...     'groups': ['wheel'],
...     'password': password
... }
>>> users.add(user_dict)
Adding user 'kevin'
>>> user_dict['groups'] = []
>>> users.update(user_dict)
Updating user 'kevin'
>>> users.remove(user_dict)
Removing user 'kevin'
>>>
```

------------------------------------------------------------------------------------------------

# 8: Json Parsing And Exporting

*tests/test_inventory.py*

```python
import tempfile

from hr import inventory

def test_inventory_load():
    """
    `inventory.load` takes a path to a file and parses it as JSON
    """
    inv_file = tempfile.NamedTemporaryFile(delete=False)
    inv_file.write(b"""
    [
      {
        "name": "kevin",
        "groups": ["wheel", "dev"],
        "password": "password_one"
      },
      {
        "name": "lisa",
        "groups": ["wheel"],
        "password": "password_two"
      },
      {
        "name": "jim",
        "groups": [],
        "password": "password_three"
      }
    ]
    """)
    inv_file.close()
    users_list = inventory.load(inv_file.name)
    assert users_list[0] == {
        'name': 'kevin',
        'groups': ['wheel', 'dev'],
        'password': 'password_one'
    }
    assert users_list[1] == {
        'name': 'lisa',
        'groups': ['wheel'],
        'password': 'password_two'
    }
    assert users_list[2] == {
        'name': 'jim',
        'groups': [],
        'password': 'password_three'
    }

def test_inventory_dump(mocker):
    """
    `inventory.dump` takes a destination path and optional list of users to export then exports the existing user information.
    """
    dest_file = tempfile.NamedTemporaryFile(delete=False)
    dest_file.close()

    # spwd.getspnam can't be used by non-root user normally.
    # Mock the implemntation so that we can test.
    mocker.patch('spwd.getspnam', return_value=mocker.Mock(sp_pwd='password'))

    # grp.getgrall will return the values from the test machine.
    # To get consistent results we need to mock this.
    mocker.patch('grp.getgrall', return_value=[
        mocker.Mock(gr_name='super', gr_mem=['bob']),
        mocker.Mock(gr_name='other', gr_mem=[]),
        mocker.Mock(gr_name='wheel', gr_mem=['bob', 'kevin']),
    ])

    inventory.dump(dest_file.name, ['kevin', 'bob'])

    with open(dest_file.name) as f:
        assert f.read() == """[{"name": "kevin", "groups": ["wheel"], "password": "password"}, {"name": "bob", "groups": ["super", "wheel"], "password": "password"}]"""
```

Notice that we had to jump through quite a few hoops to get the tests to work consistently for the `dump` function. The `test_inventory_dump` required so much mocking that it is debatable as to whether or not it’s worth the effort to test. Here’s the implementation of the module:

*src/hr/inventory.py*

```python
import grp
import json
import spwd

from .helpers import user_names

def load(path):
    with open(path) as f:
        return json.load(f)

def dump(path, user_names=user_names()):
    users = []
    for user_name in user_names:
        password = spwd.getspnam(user_name).sp_pwd
        groups = _groups_for_user(user_name)
        users.append({
            'name': user_name,
            'groups': groups,
            'password': password
        })
    with open(path, 'w') as f:
        json.dump(users, f)

def _groups_for_user(user_name):
    return [g.gr_name for g in grp.getgrall() if user_name in g.gr_mem]
```

The default list of `user_names` for the `dump` function used the same code that was used previously in the `users` module so it was extracted into a new `helpers` module to be used in both.


*src/hr/helpers.py*

```python
import pwd

def user_names():
    return [user.pw_name for user in pwd.getpwall()
            if user.pw_uid >= 1000 and 'home' in user.pw_dir]
```

Here’s the updated `users` module:

*src/hr/users.py*

```python
import pwd
import subprocess
import sys

from .helpers import user_names

def add(user_info):
    print("Adding user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'useradd',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print("Failed to add user '%s'" % user_info['name'])
        sys.exit(1)

def remove(user_info):
    print("Removing user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'userdel',
            '-r',
            user_info['name']
        ])
    except:
        print("Failed to remove user '%s'" % user_info['name'])
        sys.exit(1)

def update(user_info):
    print("Updating user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'usermod',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print("Failed to update user '%s'" % user_info['name'])
        sys.exit(1)

def sync(users, existing_user_names=user_names()):
    user_names = [user['name'] for user in users]
    for user in users:
        if user['name'] not in existing_user_names:
            add(user)
        elif user['name'] in existing_user_names:
            update(user)
    for user_name in existing_user_names:
        if not user_name in user_names:
            remove({ 'name': user_name })

def _groups_str(user_info):
    return ','.join(user_info['groups'] or [])
```

### Manually test the module

Load the Python3.6 REPL as root to interact with the new `inventory` module:

```python
$ sudo python3.6
>>> from hr import inventory
>>> inventory.dump('./inventory.json')
>>> exit()
```

Now you can look at the new `inventory.json` file to see that it dumped the users properly.

```
$ cat inventory.json
[{"name": "kevin", "groups": ["wheel"], "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"}]
```

------------------------------------------------------------------------------------------------

# 9: Creating The Console Script

Here’s an example main function that was added to the cli module:

*src/hr/cli.py*

```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to the inventory file (JSON)')
    parser.add_argument('--export', action='store_true', help='export current settings to inventory file')
    return parser

def main():
    from hr import inventory, users

    args = create_parser().parse_args()

    if args.export:
        inventory.dump(args.path)
    else:
        users_info = inventory.load(args.path)
        users.sync(users_info)
```

Here are the modifications for the `setup.py` file necessary to create a console script:

*setup.py*

```python
from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='hr',
    version='0.1.0',
    description='Commandline user management utility',
    long_description=readme,
    author='Your Name',
    author_email='person@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': 'hr=hr.cli:main',
    },
)
```

Since you need `sudo` to run the script you’ll want to install it using `sudo pip3.6`:

```
$ sudo pip3.6 install -e .
$ sudo hr --help
usage: hr [-h] [--export] path

positional arguments:
  path        the path to the inventory file (JSON)

optional arguments:
  -h, --help  show this help message and exit
  --export    export current settings to inventory file
```

------------------------------------------------------------------------------------------------

# 10: Building A Wheel Distribution

Extra metadata file:

*MANIFEST.in*

```
include README.rst
recursive-include tests *.py
```

Using the `pipenv shell`, this is the command that you would run to build the wheel:

```
(h4-YsGEiW1S) $ python setup.py bdist_wheel
```

Lastly, here's how you would install this wheel for the `root` user to be able to use (run from project directory):

```
$ sudo pip3.6 install --upgrade dist/hr-0.1.0-py3-none-any.whl
```