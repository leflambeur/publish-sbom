import argparse
import os

from archivist.archivist import Archivist

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")

def main():

    parser = argparse.ArgumentParser(description='RKVST SBOM Hub CLI Tool')
    
    parser.add_argument('--url', '-u', default='https://app.rkvst.io', help='SBOM URL to upload to')
    parser.add_argument('--publish', '-p', type=str.lower, choices=['true', 'false'], default='false', help='Publish the SBOM publicly')
    parser.add_argument('--format', '-f', choices=["cyclonedx-xml", "cyclonedx-json", "spdx-tag"], default="cyclonedx-xml", help='The SBOM format being submitted')
    parser.add_argument('--client_id', '-c', help='Specify Application CLIENT_ID inline')
    parser.add_argument('--client_secret', '-s', help='Specify Application CLIENT_SECRET inline')
    parser.add_argument('sbomfiles', metavar='<sbom-file>', nargs='+', help='SBOM to be uploaded')

    args = parser.parse_args()

    for envopt in 'client_id client_secret'.split():
        if getattr(args, envopt) is None:
            try:
                setattr(args, envopt, os.environ[f"SBOM_{envopt.upper()}"])
            except KeyError:
                print(f"use --{envopt} or set SBOM_{envopt.upper()} as an envvar")

    arch = Archivist(
        args.url,
        (args.client_id, args.client_secret),
    )
    
    for sbom in args.sbomfiles:
        print("Uploading " + sbom)
        with open(sbom, 'rb') as fd:
            visible = "PUBLIC" if str2bool(args.publish) else "PRIVATE"
            sbom_upload = arch.sboms.upload(fd, confirm=True, params={"privacy": visible, "sbomType": args.format})
            print("Uploaded", visible, sbom_upload.identity)
            print(sbom_upload)
    return

if __name__ == "__main__":
    main()
