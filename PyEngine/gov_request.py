# -*- coding: utf-8 -*-
from requests_pkcs12 import post
from cryptography.fernet import Fernet
import json
import os
#WT_add
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
key = b'NthBRA5htGkZprUpudAG-Guh5UTcbxwT50Jwvg7ePV0='
fernet = Fernet(key)


def make_header(user, userpass):
    head = {
        'Kennung': user,
        'Passwort': userpass,
        'Accept': 'text/plain; charset=UTF-8; version=6.0',
        'Content-type': 'text/plain; charset=UTF-8',
        'Content-Length': '336'
    }
    return head


def make_payload(name, surname, birth):
    #WT_version up becasue security risk if the inputs (name, surname, birth) are not properly sanitized, as it can lead to XML injection vulnerabilities.
    root = ET.Element('tns:SPIELER-SUCHPARAMETER', 
                      xmlns_ns2="http://www.hzd.de/meldungskatalogItem", 
                      xmlns_tns="http://www.hzd.de/spielerSuchparameter")
    
    spieler = ET.SubElement(root, 'SPIELER')
    ET.SubElement(spieler, 'V').text = surname
    ET.SubElement(spieler, 'N').text = name
    ET.SubElement(spieler, 'D').text = birth
    
    return ET.tostring(root, encoding='unicode', method='xml')

    #origin code
    # return '''
    #     <tns:SPIELER-SUCHPARAMETER xmlns:ns2="http://www.hzd.de/meldungskatalogItem" xmlns:tns="http://www.hzd.de/spielerSuchparameter">
    #     <SPIELER>
    #     <V>''' + surname + '''</V>
    #     <N>''' + name + '''</N>
    #     <D>''' + birth + '''</D>
    #     </SPIELER>
    #     </tns:SPIELER-SUCHPARAMETER>
    #     '''


def connect_gov(sys_id, firstname, lastname, birth):

        year = birth[6:]
        month = birth[3:5]
        day = birth[:2]

        birthday = year + '-' + month + '-' + day
        payload = make_payload(firstname, lastname, birthday)
        print(payload)

        # # load cert info file
        # file = open('certification/test.json', 'r')
        # data = json.load(file)
        #
        # url = data['url']
        #
        # head = make_header(data['user'], data['userpass'])
        # cert_pass = data['certpass']

        if os.path.exists(ROOT_DIR + '/cert_files/cert_info.bin'):
            info_filepath = ROOT_DIR + '/cert_files/cert_info.bin'
            cert_filepath = ROOT_DIR + '/cert_files/cert_file.p12'
        else:
            info_filepath = ROOT_DIR + '/cert_files/test.bin'
            cert_filepath = ROOT_DIR + '/cert_files/test.p12'
        #origin data
        # file = open(info_filepath, 'rb')
        # data = file.read()
        # decrypted_data = fernet.decrypt(data).decode()

        #WT_except handle
        try:
            with open(info_filepath, 'rb') as file:
                data = file.read()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return "Certificate information file not found"
        except Exception as e:
            print(f"Error reading file: {e}")
            return "Error reading certificate information file"

        try:
            fernet = Fernet(fernet_key)
            decrypted_data = fernet.decrypt(data).decode()
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return "Error decrypting certificate information"

        data_list = decrypted_data.split('***')
        url = data_list[0]
        user = data_list[1]
        userpass = data_list[2]
        cert_pass = data_list[3]

        head = make_header(user, userpass)

        print("--- Ready to send request ---")

        # Send request
        try:
            Resp = post(url, data= payload, headers=head , pkcs12_filename=cert_filepath, pkcs12_password=cert_pass, verify=True) # If you need a response package To verify, you need to pass the verification
            Resp.raise_for_status() 

            text = Resp.text
            tem = text.split('<MELDUNG>')[1]
            res = tem.split('</MELDUNG>')[0]

            print(res)
            return res

        except IndexError as e:
            print(f"Error processing response: {e}")
            return "Error processing response"       

if __name__ == '__main__':
    firstname = 'Ismail'
    lastname = 'Tuna'
    birth = '10.05.1971'

    # key = b'NthBRA5htGkZprUpudAG-Guh5UTcbxwT50Jwvg7ePV0='
    # fernet = Fernet(key)
    try:
        result = connect_gov('12', firstname, lastname, birth)
        print(result)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
