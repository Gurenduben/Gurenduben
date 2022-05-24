#!/usr/bin/python
 
#################################################################################
#                                                                               #
#.______               _______.  ______     ___      .__   __.                  #
#|   _  \             /       | /      |   /   \     |  \ |  |                  #
#|  |_)  |    ______ |   (----`|  ,----'  /  ^  \    |   \|  |                  #
#|      /    |______| \   \    |  |      /  /_\  \   |  . `  |                  #
#|  |\  \----.    .----)   |   |  `----./  _____  \  |  |\   |                  #
#| _| `._____|    |_______/     \______/__/     \__\ |__| \__|  v0.2.0          #
#                                                                               #
#GNU PL - 2015 - ca333  (modified by simcity4242)                               #
#                                                                               #
#USE AT OWN RISK!                                                               #
#################################################################################
 
import json
import urllib2
import time
import sys
 
#for some reason blockchain.info api-chain is 59711 blocks short..
#blockstart = 170399
#blockstart += 59711
#blockcount = urllib2.urlopen("https://b...content-available-to-author-only...n.info/en/q/getblockcount").read()
 
def rscan(addr):
    """Check address for duplicated r values."""
    # TODO: add BCI API check address
 
    print "WELCOME TO R-scan v0.1.2!"
    print "ADDRESS-R-SCAN: "
     
    urladdr = 'https://b...content-available-to-author-only...n.info/address/%s?format=json&offset=%s'
 
    ###control api-url
    #print str(urladdr[:-22] % addr)
 
    addrdata = json.load(urllib2.urlopen(urladdr % (addr, '0')))
    ntx = addrdata['n_tx']
    print "Data for pubkey: " + str(addr) + " has " + str(addrdata['n_tx']).center(6) + "Tx%s" % 's'[ntx==1:]
    #print "number of txs: " + str(addrdata['n_tx'])
 
    #tx-details:
 
    txs = []
    for i in range(0, ntx//50 + 1):
        sys.stderr.write("Fetching Txs from offset\t%s\n" % str(i*50))
        jdata = json.load(urllib2.urlopen(urladdr % (addr, str(i*50))))
        txs.extend(jdata['txs'])    
 
    assert len(txs) == ntx
    addrdata['txs'] = txs
 
 
    y = 0
    inputs = []
    while y < ntx:   
        #print "77379c0674c92db63f019e163607bc7b7533a69a889d04332a53a8c00e3dbcdf"
        #print "TX nr :" + str(y+1)
        #print "hash: " + str(addrdata['txs'][y]['hash'])
        #print "number of inputs: " + str(addrdata['txs'][y]['vin_sz'])
        #only if
        #if addrdata['txs'][y]['vin_sz'] > 1:
        zy = 0
        while zy < addrdata['txs'][y]['vin_sz']:
            #print "Input-ScriptNR " + str(zy+1) + " :" + str(addrdata['txs'][y]['inputs'][zy]['script'])
            inputs.append(addrdata['txs'][y]['inputs'][zy]['script'])
            zy += 1
        y += 1
 
    xi = 0
    zi = 1
    lenx = len(inputs)
    alert = 0
     
    bad = []
    #compare the sig values in each input script
    while xi < lenx-1:
        x = 0
        while x < lenx-zi:
            if inputs[xi][10:74] == inputs[x+zi][10:74]:
                #print "In Input NR: " + str(xi) + "[global increment] " + str(inputs[xi])
                #print('\a')
                print "Resued R-Value: "
                print inputs[x+zi][10:74]
                bad.append((int(x), str(inputs[x+zi][10:74])))
                alert += 1
            x += 1
            zi += 1
        xi += 1
 
    #check duplicates
    #alert when everything ok
 
    if alert < 1:
        print "Good pubKey. No problems."
    else:
        print "Address %s has %d reused R value%s!" % (addr, len(bad), "s"[len(bad)==1:])
        return bad
         
if __name__ == '__main__':
    from sys import argv
    print """python rscan.py 155M7TvBRww6WFdtGQgTYUH8DuLheNafCf"""
    if len(argv) == 1:
        addr = raw_input("Enter Bitcoin address eg 155M7TvBRww6WFdtGQgTYUH8DuLheNafCf")
    elif len(argv) == 2 and isinstance(argv[1], basestring):
        addr = str(argv[1])
    rscan(addr)
     
# 77379c0674c92db63f019e163607bc7b7533a69a889d04332a53a8c00e3dbcdf