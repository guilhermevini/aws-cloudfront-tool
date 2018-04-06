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

    return input("\tEscolha uma opção: ")

dists = [0]*10

def show_distributions():
    display_title_bar()
    response = client.list_distributions()
    list = response['DistributionList']
    count=0
    for dist in list['Items']:
        id = dist['Id']
        print("\t[%s] " % count + id)
        dists[count]=id
        count +=1
        for domain in dist['Aliases']['Items']:
            print("\t" + domain)
        print("\n")

    option = input("\tQual cache deseja limpar? ")
    path = input("\tCaminho do arquivo ou pattern: ")

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
