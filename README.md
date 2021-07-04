## Program to auto search errors

The purpose of this program is to find out the error in your code and then look up for Stack overflow pages that are solving the same or somewhat similar queries.\
To run the code, first of all , we will have to install a few libraries. You can install them using the pip command from anaconda command prompt or the terminal of any IDE.\
To import the package,
```python
import shlex
import requests
from subprocess import Popen, PIPE
import webbrowser
import Levenshtein
```

You will have to enter your code in the test.py file.\
Now we will split the output and error part away. If the code does not have any error, then it will simply print the output.\
If it encounters any error , then we will enter the error and create a stack overflow API link.\
```python
def find_solution(error):
    print("Searching for " + error)
    resp = requests.get(
        "https://api.stackexchange.com/" + "2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(
            error))
    return resp.json()
```
The homepage of the Stack Overflow API is [here](https://api.stackexchange.com/docs).

\
This will give us a json file consisting of various questions that have a similar error.\
We will extract the links out of all of them and sort them based on their views plus the API will have automatically sorted them based on their relevance.
```python
def get_urls(json_dict, err_msg):
    count = 0
    link_store = {}
    d = []
    for i in json_dict['items']:
        if i["is_answered"]:
            count += 1
            link_store[count] = i["link"]
            x = Levenshtein.ratio(err_msg, i["title"])
            d.append([x, count])
        if count == 10:
            break
    d.sort(key=lambda x: (-x[0], x[1]))
```

We will open the top 3 most viewed+relevant posts on the Stack Overflow website that have a similar error.