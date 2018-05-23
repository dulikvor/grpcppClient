import argparse
import curses
from grpcppClient.Configuration import Configuration
from grpcppClient.Parser import Lexer
from grpcppClient.Terminal import *

def main():
    parser = argparse.ArgumentParser(description='grpc client.')
    parser.add_argument('--idl', help='grpc idl file location.')
    args = parser.parse_args()

    config = Configuration()
    config.LoadParams(IDL_LOCATION = args.idl)

    lexer = Lexer()
    lexer.ParseSchema(config.GetParam('IDL_LOCATION'))

if __name__== "__main__":
    with CursesConfigure():
        terminal = Terminal()
        terminal.start()
        terminal.waitForCompletion()
        main()
