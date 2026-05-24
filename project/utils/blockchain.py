"""
Blockchain Integration Module
Simulates blockchain for certificate verification
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any
import uuid

class Block:
    """Individual block in blockchain"""
    
    def __init__(self, index: int, transactions: List[Dict], timestamp: str, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA256 hash of block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Proof of work mining"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class BlockchainVerifier:
    """Blockchain for land certificates"""
    
    def __init__(self, difficulty: int = 2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
    
    def create_genesis_block(self) -> Block:
        """Create first block"""
        return Block(0, [], datetime.now().isoformat(), "0")
    
    def get_latest_block(self) -> Block:
        """Get most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict) -> int:
        """Add transaction to pending list"""
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1
    
    def mine_pending_transactions(self) -> Block:
        """Mine all pending transactions"""
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=datetime.now().isoformat(),
            previous_hash=self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return block
    
    def register_land_certificate(self, certificate_id: str, land_data: Dict) -> str:
        """Register a land certificate on blockchain"""
        transaction = {
            'id': str(uuid.uuid4()),
            'type': 'LAND_CERTIFICATE',
            'certificate_id': certificate_id,
            'farmer_name': land_data.get('farmer_name'),
            'land_id': land_data.get('land_id'),
            'grid_position': land_data.get('grid_position'),
            'crop_type': land_data.get('crop_type'),
            'area_acres': land_data.get('area_acres'),
            'timestamp': datetime.now().isoformat(),
            'hash': hashlib.sha256(json.dumps(land_data).encode()).hexdigest()
        }
        
        self.add_transaction(transaction)
        block = self.mine_pending_transactions()
        return block.hash
    
    def verify_certificate(self, certificate_id: str) -> Dict[str, Any]:
        """Verify if certificate exists on blockchain"""
        for block in self.chain:
            for tx in block.transactions:
                if tx.get('certificate_id') == certificate_id:
                    return {
                        'verified': True,
                        'block_index': block.index,
                        'block_hash': block.hash,
                        'transaction': tx,
                        'timestamp': block.timestamp,
                        'confirmations': len(self.chain) - block.index
                    }
        return {'verified': False, 'message': 'Certificate not found'}


class CertificateNFT:
    """NFT-like certificate representation"""
    
    def __init__(self, certificate_data: Dict):
        self.certificate_id = certificate_data['certificate_id']
        self.metadata = {
            'name': f"Land Certificate {certificate_data['certificate_id']}",
            'description': f"Verified land ownership for {certificate_data['farmer_name']}",
            'image': f"/api/certificate/{certificate_data['certificate_id']}/qr",
            'attributes': [
                {'trait_type': 'Farmer Name', 'value': certificate_data['farmer_name']},
                {'trait_type': 'Land ID', 'value': certificate_data['land_id']},
                {'trait_type': 'Grid Position', 'value': certificate_data['grid_position']},
                {'trait_type': 'Crop Type', 'value': certificate_data['crop_type']},
                {'trait_type': 'Area (Acres)', 'value': certificate_data['area_acres']},
                {'trait_type': 'Verification Date', 'value': certificate_data['timestamp']}
            ]
        }
        self.metadata_hash = hashlib.sha256(json.dumps(self.metadata).encode()).hexdigest()
    
    def to_json(self) -> Dict:
        """Convert to JSON format"""
        return {
            'certificate_id': self.certificate_id,
            'metadata': self.metadata,
            'metadata_hash': self.metadata_hash
        }