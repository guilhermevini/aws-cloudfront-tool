# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import boto3
import time

client = boto3.client('cloudfront')

def display_title_bar():
    os.system('clear')

    print("\n\n")

    print("\t**********************************************")
    print("\t***         cdn and cache control          ***")
    print("\t**********************************************")
    print("\n")

def get_user_choice():
    print("\t[1] Listar Distribuições.")
    print("\t[q] Sair.")
    print("\n")

    return raw_input("\tEscolha uma opção: ")


def show_distributions():
    display_title_bar()

    response = client.list_distributions()
    dlist = response['DistributionList']
    
    dists = []
    count=0

    for dist in dlist['Items']:
        id = dist['Id']
        print("\t[%s] " % count + id + " (" + dist['Status'] + ")")
        print("\t"+ dist['DomainName'])

        dists.insert(count, id)
        count +=1

        if ('Items' in dist['Aliases']): 
            for domain in dist['Aliases']['Items']:
                print("\t" + domain)
        else:
            for domain in dist['Origins']['Items']:
                print("\t" + domain['DomainName'])
        print("\n")

    option = raw_input("\tQual cache deseja limpar? (ou 'q' para sair): ")
    if option == 'q':
        print("\n")
        return
    path = raw_input("\tCaminho do arquivo ou pattern: ")

    if len(dists) >= int(option):
        selected = dists[int(option)]
        print("\n\tCache Zerado: %s" % selected)
        invalidation = client.create_invalidation(DistributionId=selected,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [path]
            },
            'CallerReference': str(time.time())
        })
        print("\tStatus: %s" % invalidation['Invalidation']['Status'])
        print("\n")
    else:
        show_distributions()

def menu():
    if choice == '1':
        show_distributions()
    elif choice == 'q':
        print("\n\tVolte sempre!")
    else:
        print("\n\tOpção Inválida.")

display_title_bar()
choice = get_user_choice()
menu()
