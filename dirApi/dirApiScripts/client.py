#!/usr/bin/env python3

'''
    REST access library + client example
'''

from restDir.client import Directory

def main():
    ''' Entry point '''
    client = Directory('http://127.0.0.1:3002/')
    #print(client.remove_file('c5da5fc2-5d28-11ed-9d03-dd969f8236ef', 'file'))
    #print(client.new_file('c5da5fc2-5d28-11ed-9d03-dd969f8236ef', 'file', '/dir1/file'))
    #print(client.get_file('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','file2'))
    #print(client.list_files('c5da5fc2-5d28-11ed-9d03-dd969f8236ef'))
    #print(client.remove_directory('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','dir6'))
    #print(client.new_directory('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','dir6'))
    #print(client.list_directories('c5da5fc2-5d28-11ed-9d03-dd969f8236ef'))

if __name__ == '__main__':
    main()