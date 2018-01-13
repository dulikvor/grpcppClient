import argparse
from grpcppClient.Configuration import Configuration

def main():
    parser = argparse.ArgumentParser(description='grpc client.')
    parser.add_argument('--idl', help='grpc idl file location.')
    args = parser.parse_args()

    config = Configuration()
    config.LoadParams(IDL_LOCATION = args.idl)

if __name__== "__main__":
    main()