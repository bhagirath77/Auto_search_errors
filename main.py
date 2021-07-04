import shlex
import requests
from subprocess import Popen, PIPE
import webbrowser
import Levenshtein


def execute_and_return(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


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
    for i in range(min(3, len(d))):
        webbrowser.open(link_store[d[i][1]])


def find_solution(error):
    print("Searching for " + error)
    resp = requests.get(
        "https://api.stackexchange.com/" + "2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(
            error))
    return resp.json()


if __name__ == "__main__":
    opt, err = execute_and_return("python test.py")
    opt = opt.decode("utf-8").strip().split("\r\n")
    err_msg = err.decode("utf-8").strip().split("\r\n")[-1]
    if err_msg:
        json = find_solution(err_msg)
        get_urls(json, err_msg)
        print("Hope you got your problem solved :)")

    else:
        print("No errors, output is: \n")
        print(*opt, sep="\n")
