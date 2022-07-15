import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(
                        proof = 1, 
                        prevHash = '0')
    
    def createBlock(self, proof, prevHash, data):
        block = {
            'index':        (len(self.chain) + 1),
            'timestamp':    str(datetime.datetime.now()),
            'data':         data,
            'proof':        proof,
            'prevHash':     prevHash 
        }
        self.chain.append(block)
        return block

    def getPrevBlock(self):
        return self.chain[-1] 

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False

        while checkProof is not True:
            hashOp = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()

            if hashOp[0:4] == '0000':
                checkProof = True
            else:
                newProof += 1

        return newProof 


    def hash(self, block):
        encodedBlock = json.dumps(
                            obj = block,
                            sort_keys=True
        )
        hash = hashlib.sha256(encodedBlock.encode()).hexdigest()

    def isChainValid(self):
        prevBlock = self.chain[0]
        for blockNum in range(2, len(self.chain)):
            block = self.chain[blockNum]
            if block['prevHash'] != self.hash(prevBlock):
                return False

            prevProof = prevBlock['proof']
            hashOp = hashlib.sha256(str(block['proof']**2 - prevProof**2).encode()).hexdigest()
            if hashOp[0:4] != '0000':
                return False
            
            prevBlock = block
        
        return True

        






app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
