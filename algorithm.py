import chess.pgn
import random
import chess
import math
import subprocess
import os
import re
from Gaussian import Gaussian

CMD = [os.getcwd()+os.sep+"pgn-extract.exe", "-P",
            "-vinput.txt","--selectonly","1","database.pgn"]
INPUT = os.getcwd()+os.sep+"input.txt"

def descent(node): 
    if(node.visited): 
        child =  node.getChild()
        if(child!=None): 
            #update message from parent
            score = child.gDis /child.messageFromParent 
            messageFromParent = node.gDis/child.messageToParent+Gaussian(0,1)
            child.messageFromParent = messageFromParent
            child.gDis= score * messageFromParent
            #continue descent 
            messageToParent = descent(child)
            #update message to parent
            score_node = node.gDis/child.messageToParent
            node.gDis = score_node * messageToParent
            child.messageToParent = messageToParent
    else:
        #update message from parent 
        node.parent.gDis = node.parent.gDis / node.parent.rollOut
        node.parent.rollOut = Gaussian()
        score = node.gDis / node.messageFromParent
        messageFromParent = node.parent.gDis / node.messageToParent+Gaussian(0,1)
        node.messageFromParent = messageFromParent
        node.gDis = score * messageFromParent
        #do roll-out
        (result,length) = rollOut(node)
        messageFromRollOut = rollOutMessage(result,length,node)
        if(length==0):
            node.gDis = messageFromRollOut
        else:
            node.gDis = node.gDis * messageFromRollOut

        node.rollOut = messageFromRollOut
        node.visited = True
    return  (node.gDis / node.messageFromParent) +  Gaussian(0,1)

def getSans(node,san_moves):
    if(node.parent==None):
        return
    else:
        getSans(node.parent,san_moves)
        san_moves.append(node.san())
def rollOut(node):
    input_file = open(INPUT,"w")
    #get san moves
    san_moves = []
    getSans(node,san_moves)
    #write into file
    print node.board()
    input_file.write(" ".join(san_moves))
    input_file.close()
    #search one match game
    proc = subprocess.Popen(CMD,stdout=subprocess.PIPE)
    result = proc.communicate()[0]
    #get length
    groups  = re.findall(r"(\d*)\.",result)
    if(not groups):
        return -1,1
    length = int(groups[-1])
    #get result
    m = re.search(r'Result \"(.*)\"',result)
    if(m.group(1) == "1-0"):
        result = 1
        length = length*2-1
    else:
        result = -1
        length = length*2

    return  result,length

def rollOutMessage(result,length,node): 
    prior = node.gDis + Gaussian(0,length)
    prior_sigma = math.sqrt(prior.var)
    #posterior moment matching
    if(result > 0):
        k = float(prior.mean)/float(prior_sigma)
        b = float(Gaussian.pdf(k))/float(Gaussian.phi(k))
        firstMoment = prior.mean + prior_sigma*b
        secondMoment = pow(prior.mean,2)+prior.var*(1+k*b)
    else:
        k = float(prior.mean)/float(prior_sigma)
        b = float(Gaussian.pdf(k))/float(Gaussian.phi(-k))
        firstMoment =  prior.mean - prior_sigma*b
        secondMoment = pow(prior.mean,2)+prior.var*(1-k*b)

    posterior = Gaussian(firstMoment,secondMoment-pow(firstMoment,2))   
    return posterior+Gaussian(0,length)
    
