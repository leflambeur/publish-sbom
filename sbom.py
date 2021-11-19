from archivist import archivist
import sys
import json
import argparse
import os
import requests

def generate_token(client_id, client_secret, rkvst_url):

    print("Found Credentials")

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        
    }

    token_endpoint = rkvst_url + '/archivist/iam/v1/appidp/token'

    print("Generating Token")
    token_request = requests.post(token_endpoint, headers=headers, data=params).json()

    return token_request.get("access_token")

def upload_sbom(arch, sbom_files):
#no_publish
    for sbom in sbom_files:
        with open(sbom) as fd:
            sbom_upload = arch.sboms.upload(fd)
            print(sbom_upload)
        #if no_publish == False:
         #   arch.sboms.publish(sbom_upload)

def main():

    parser = argparse.ArgumentParser(description='RKVST for SBOM CLI Tool')
    
    parser.add_argument('--url', '-u', default='https://sbom.rkvst.io', help='SBOM URL to upload to')
    #parser.add_argument('--no-publish', dest='no_publish', action='store_true', help='Upload an SBOM without publishing')
    parser.add_argument('sbomFiles', metavar='<sbom-file>', nargs='+', help='SBOM to be uploaded')

    client_group = parser.add_mutually_exclusive_group(required=True)
    client_group.add_argument('--clientId', '-c', nargs=1, help='Specify Application CLIENT_ID inline')
    client_group.add_argument('--envClientId', '-i', action='store_true',  help='Specify if your Application CLIENT_ID is an Env Var')

    secret_group = parser.add_mutually_exclusive_group(required=True)
    secret_group.add_argument('--secret', '-s', nargs=1, help='Specify Application SECRET inline')
    secret_group.add_argument('--envSecret', '-e', action='store_true',  help='Specify if your Application SECRET is an Env Var')

    args = parser.parse_args()

    if args.envClientId == True:
        try:
            client_id = os.getenv("CLIENT_ID")
        except:
            exit(
                "ERROR: CLIENT_ID EnvVar not found"
            )
    else:
        client_id = args.clientId

    if args.envSecret == True:
        try:
            client_secret= os.getenv("SECRET")
        except:
            exit(
                "ERROR: SECRET EnvVar not found"
            )
    else:
        client_secret = args.secret

    rkvst_url = args.url

    try:
            authtoken = generate_token(client_id, client_secret, rkvst_url)
    except:
        exit(
            "ERROR: Auth token not found. Please check your CLIENT_ID and AUTH_TOKEN."
        )

    print("Token Generated")

    sbom_files = args.sbomFiles

    print(args.sbomFiles)

    arch = archivist.Archivist(
        rkvst_url,
        auth=authtoken,
        )
# args['no-publish']
    try:    
        upload_sbom(arch, sbom_files)
    except:
        exit(
            "ERROR: Failed to Upload SBOMS"
            )

if __name__ == "__main__":
    main()
