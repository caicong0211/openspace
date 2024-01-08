import hashlib
import json
from time import time
from typing import Any,Dict,List,Optional


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        #创建创世块
        self.new_block(previous_hash='1',proof=100)
    
    def new_block(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:
        """
        生成新块
        -> Dict[str, Any]:表示此方法返回类型是字典类型
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
       
        block = {
             'index': len(self.chain)+1,
             'timestamp': time(),
             'transaction':self.current_transactions,
             'proof':proof,
             'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
        
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self,sender:str,recipient:str,amount:int)->int:
        """
        生成新的交易信息，信息将加入到下一个代挖的区块中
        :param sender: address of the sender
        :param recipient: address of the recipient
        :para, amount: amount
        :return: the index of the block that will hold this transcation
        """
        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount,
        })
        return self.last_block['index'] + 1
    
    @property
    def last_block(self) -> Dict[str,Any]:
        return self.chain[-1]
    
    @staticmethod
    def hash(block: Dict[str,Any]) ->str:
        """
        生成块的sha-256 hash 值
        :param block:Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block,sort_keys=True).encode()
        """
        将字典转换为 JSON 格式的字符串，并确保字典的键是有序的。
        """
        return hashlib.sha256(block_string).hexdigest()
        """
        返回sha256计算block里的值的数据,hexdigest将2进制转为16进制。
        """

    def proof_of_work(self,last_block:int) -> int:
        """
        简单的工作量证明：
        -查找一个p'使得hash(pp')以4个0开头
        -p是上一个块的证明.p'是当前的证明
        """

        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1
        return proof
        """
         valid_proof 方法：
         self.valid_proof(last_proof, proof) 用于验证给定的证明是否符合条件。这个方法的具体实现在你提供的代码中可能有，但在当前提供的代码片段中未包含。
         通常，这个方法会计算 hash(last_proof, proof) 并检查是否以4个0开头。
        """

    @staticmethod 
    def valid_proof(last_proof: int, proof: int)->bool:
        """
        验证证明:是否hash(last_proof,proof)以4个0开头
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: true if correct, false if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
blockchain = Blockchain()

blockchain.new_transaction(
        sender="0",
        recipient="harbour",
        amount=1,
        )

blockchain.new_transaction(
        sender="harbour",
        recipient="openspace",
        amount=100,
        )
    
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)

blockchain.new_block(proof, None)

print(json.dumps(blockchain.chain, sort_keys=True))

