## 1. Handling Errors When Files Don't Exist:

Write a script that does the following:

-   Receives a `file_name` and `line_number` as command line parameters.
-   Prints the specified `line_number` from `file_name` to the screen. The user will specify this as you would expect, not using zero as the first line.

Make sure that you handle the following error cases by presenting the user with a useful message:

1.  The file doesn't exist.
2.  The file doesn't contain the `line_number` specified (file is too short).

----------------------------------

## 2. Interacting With External Commands:

It's not uncommon for a process to run on a server and listen to a port. Unfortunately, you sometimes don't want that process to keep running, but all you know is the port that you want to free up. You're going to write a script to make it easy to get rid of those pesky processes.

Write a script that does the following:

-   Takes a `port_number` as its only argument.
-   Calls out to `lsof` to determine if there is a process listening on that port.
    -   If there is a process, kill the process and inform the user.
    -   If there is no process, print that there was no process running on that port.

Python's standard library comes with an HTTP server that you can use to start a server listening on a port (5500 in this case) with this line:
```
$ python -m http.server 5500
```

Use a separate terminal window/tab to test our your script to kill that process.

*Hints:*

-   You may need to install `lsof`. Use this command on CentOS:
    ```
    $ sudo yum install -y lsof
    ```

-   Use this line of `lsof` to get the port information:
    ```
    lsof -n -i4TCP:PORT_NUMBER
    ```

    That will return multiple lines, and the line you want will contain "LISTEN".
-   Use the string `split()` method to break a string into a list of its words.
-   You can either use the `kill` command outside of Python or the `os.kill(pid, 9)` function.

----------------------------------

## 3. Setting Exit Status On Errors

You’ve now written a few scripts that handle errors, but when the failures happen the status code returned is still a success (0).

Improve your script to kill processes by exiting with an error status code when there isn’t a process to kill.

----------------------------------

## 4. Utilizing Third-Party Packages

Make sure that you have the `requests` package installed. Now, write a script that does the following:

-   Accepts a URL and destination file name from the user calling the script.
-   Utilizes `requests` to make an HTTP request to the given URL.
-   Has an optional flag to state whether or not the response should be JSON or HTML (HTML by default).
-   Writes the contents of the page out to the destination.

*Note:* You'll want to use the `text` attribute to get the HTML.

----------------------------------

## 5. Creating a Python Project

Over the course of the next few exercises, you'll be creating a Python package to manage users on a server based on an "inventory" JSON file. The first step in this process is going to be setting up the project's directory structure and metadata.

Do the following:

1.  Create a project folder called `hr` (short for "human resources").
2.  Set up the directories to put the project's source code and tests.
3.  Create the `setup.py` with metadata and package discovery.
4.  Utilize `pipenv` to create a virtualenv and Pipfile.
5.  Add `pytest` and `pytest-mock` as development dependencies.
6.  Set the project up in source control and make your initial commit.

----------------------------------

## 6. Test Drive Building A Cli Parser

The ideal usage of the `hr` command is this:

```
$ hr path/to/inventory.json
Adding user 'kevin'
Added user 'kevin'
Updating user 'lisa'
Updated user 'lisa'
Removing user 'alex'
Removed user 'alex'
```

The alternative usage of the CLI will be to pass a `--export` flag like so:

```
$ hr --export path/to/inventory.json
```

This `--export` flag won't take any arguments. Instead, you'll want to default the value of this field to `False` and set the value to `True` if the flag is present. Look at the [action documentation](https://docs.python.org/2.7/library/argparse.html#action) to determine how you should go about doing this.

For this exercise, Write a few tests before implementing a CLI parser. Ensure the following:

1.  An error is raised if no arguments are passed to the parser.
2.  No error is raised if a path is given as an argument.
3.  The `export` value is set to `True` if the `--export` flag is given.

----------------------------------

## 7. Implementing User Management

*Note:* This exercise is large and could take some time to complete, but don't get discouraged.

The tool you're building is going to be running on Linux systems, and it's safe to assume that it's going to run via `sudo`. With this information, it's safe to say that the tool can utilize `usermod`, `useradd`, and `userdel` to keep users on the server up to date.

Create a module in your package to work with user information. You'll want to be able to do the following:

1.  Received a list of user dictionaries and ensure that the system's users match.
2.  Have a function that can create a user with the given information if no user exists by that name.
3.  Have a function that can update a user based on a user dictionary.
4.  Have a function that can remove a user with a given username.
5.  The create, update, and remove functions should print that they are creating/updating/removing the user before executing the command.

The user information will come in the form of a dictionary shaped like this:

```
{
  'name': 'kevin',
  'groups': ['wheel', 'dev'],
  'password': '$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/'
}
```

The `password` values will be SHA512 encrypted.

*Hint:* You can generate an encrypted password in Python that is usable with `usermod -p` with this snippet:

```
import crypt

crypt.crypt('password', crypt.mksalt(crypt.METHOD_SHA512))
```

Tools to Consider:
------------------

You'll likely want to interface with the following Unix utilities:

-   `useradd`
-   `usermod`
-   `userdel`

Python modules you'll want to research:

-   `pwd` - Password/User database.
-   `grp` - Group database.

Be careful in testing not to delete your own user or change your password to something that you don't know.

----------------------------------

## 8. JSON Parsing And Exporting

Note: This exercise is large and could take some time to complete, but don't get discouraged.

The last module that you’ll implement for this package is one for interacting with the user inventory file. The inventory file is a JSON file that holds user information. The module needs to:

1. Have a function to read a given inventory file, parse the JSON, and return a list of user dictionaries.
2. Have a function that takes a path, and produces an inventory file based on the current state of the system. An optional parameter could be the specific users to export.

Python modules you’ll want to research:

`json` - Interact with JSON from Python.
`grp` - Group database.
`pwd` - Password/user database.
`spwd` - Shadow Password database. (Used to get current encrypted password)

Example inventory JSON file:

```json
[
  {
    "name": "kevin",
    "groups": ["wheel", "dev"],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  },
  {
    "name": "lisa",
    "groups": ["wheel"],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  },
  {
    "name": "jim",
    "groups": [],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  }
]
```

*Hint*: If you’re writing tests for this code you’ll need to heavily rely on mocking to make the interactions with modules like `grp`, `pwd`, and `spwd` consistent.

----------------------------------

## 9. Creating The Console Script

Now that you've implemented all of the functionality that the `hr` tools needs, it's time to wire the pieces together and modify the package metadata to create a console script when installed.

1.  Implement `main` function that ties all of the modules together based on input to the CLI parser.
2.  Modify the `setup.py` so that when installed there is an `hr` console script.

----------------------------------

## 10. Building A Wheel Distribution

Now that you know the tool works, it’s time to build it for distribution. Build a wheel for the package and use it to install the hr tool on your system.

Note: This package doesn’t support Python 2, so it is not a “universal” package.