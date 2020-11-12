import sys
import os


def main():
    solr_index_envs = []
    print(sys.argv)
    if len(sys.argv) > 1:
        # solr_index_envs = string.split(sys.argv[1], ',')
        solr_index_envs = sys.argv[1].split(',')
        print(solr_index_envs)
    else:
        print('No arguments provided!')


if __name__ == '__main__':
    main()
