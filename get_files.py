from urllib import request
import json
import os


def get_files(user: str, credential: str, datastream: str, start: str, end: str, output=None):

    # combine user and credential
    username = "{}:{}".format(user, credential)

    # start and end strings for query_url are constructed
    if start: start = "&start={}".format(start)
    if end: end = "&end={}".format(end)

    # build link, user = username:credentials, datastream can be partial, start and end in form YYYY-MM-DD
    query_url = 'https://adc.arm.gov/armlive/livedata/query?user={0}&ds={1}{2}{3}&wt=json'\
        .format(username, datastream, start, end)
    print("query url = {}".format(query_url))

    # get url response, read the body of the message, and decode from bytes type to utf-8 string
    response_body = request.urlopen(query_url).read().decode("utf-8")
    # if the response is an html doc, then there was an error with the user
    if response_body[1:14] == "!DOCTYPE html":
        print("Error with user. Check username or token.")
        exit(1)

    # parse into json object
    response_body_json = json.loads(response_body)
    print("response body:\n{0}\n".format(json.dumps(response_body_json, indent=True)))

    # construct output directory
    if output:
        # output files to directory specified
        output_dir = os.path.join(output)
    else:
        # if no folder given, add datastream folder to current working dir to prevent file mix-up
        output_dir = os.path.join(os.getcwd(), datastream)

    # response is successful and files were returned
    if response_body_json["status"] == "success" and len(response_body_json["files"]) > 0:
        for f in response_body_json['files']:
            print("[DOWNLOADING] {}".format(f))
            # construct link to web service saveData function
            save_data_url = "https://adc.arm.gov/armlive/livedata/saveData?user={0}&file={1}"\
                .format(username, f)
            print("downloading file: {0}\n\tusing link: {1}".format(f, save_data_url))

            output_file = os.path.join(output_dir, f)
            # make directory if it doesn't exist
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            # create file and write bytes to file
            with open(output_file, 'wb') as open_bytes_file:
                open_bytes_file.write(request.urlopen(save_data_url).read())
            print("file saved to --> {}\n".format(output_file))
    else:
        print("No files returned or url status error.\nCheck datastream name, start, and end date.")

I tested it from my computer. It is possible that there might be some issues using the urllib.request module, it can be buggy in some cases. I used it so that you wouldn't have to import a 3rd party module (namely 'requests'). If you have trouble with this code please let me