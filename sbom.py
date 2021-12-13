from archivist.archivist import Archivist
import argparse
import os


def upload_sbom(arch, sbom_files, no_publish):
#no_publish
    for sbom in sbom_files:
        print("Uploading " + sbom)
        with open(sbom, 'rb') as fd:
            if no_publish == False:
                sbom_upload = arch.sboms.upload(fd, params={"privacy": "PUBLIC"})
                print("Uploaded " + sbom_upload.identity + " Publicly")
            else:
                sbom_upload = arch.sboms.upload(fd, params={"privacy": "PRIVATE"})
                print("Uploaded " + sbom_upload.identity + " Privately")
            print(sbom_upload)
    return

def main():

    parser = argparse.ArgumentParser(description='RKVST for SBOM CLI Tool')
    
    parser.add_argument('--url', '-u', default='https://sbom.rkvst.io', help='SBOM URL to upload to')
    parser.add_argument('--noPublish', action='store_true', help='Upload an SBOM without publishing')
    parser.add_argument('sbomFiles', metavar='<sbom-file>', nargs='+', help='SBOM to be uploaded')

    client_group = parser.add_mutually_exclusive_group(required=True)
    client_group.add_argument('--clientId', '-c', nargs=1, help='Specify Application CLIENT_ID inline')
    client_group.add_argument('--envClientId', '-i', action='store_true',  help='Specify if your Application CLIENT_ID is an Env Var')

    secret_group = parser.add_mutually_exclusive_group(required=True)
    secret_group.add_argument('--secret', '-s', nargs=1, help='Specify Application SECRET inline')
    secret_group.add_argument('--envSecret', '-e', action='store_true',  help='Specify if your Application SECRET is an Env Var')

    args = parser.parse_args()

    if args.envClientId == True:
        client_id = os.getenv("CLIENT_ID")
        if client_id is None:
            exit(
                "ERROR: CLIENT_ID EnvVar not found"
            )
    else:
        client_id = args.clientId

    if args.envSecret == True:
        client_secret= os.getenv("SECRET")
        if client_secret is None:
            exit(
                "ERROR: SECRET EnvVar not found"
            )
    else:
        client_secret = args.secret

    rkvst_url = args.url

    
    arch = Archivist(
        rkvst_url,
        (client_id, client_secret),
    )

    print("Token Generated")

    sbom_files = args.sbomFiles

    print(args.sbomFiles)

    upload_sbom(arch, sbom_files, args.noPublish)


if __name__ == "__main__":
    main()
