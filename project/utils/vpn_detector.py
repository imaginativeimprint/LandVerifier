"""
Advanced VPN/Proxy Detection Module
No external DNS dependencies - uses simple socket and HTTP APIs
"""

import socket
import requests
from typing import Tuple, Dict, Any
from datetime import datetime

class VPNDetector:
    """Multi-layer VPN detection system"""
    
    def __init__(self):
        self.common_vpn_ports = [1194, 1723, 500, 4500, 1701, 1433]
    
    def check_ip_blacklist(self, ip: str) -> Tuple[bool, str]:
        """Check IP against known blacklists"""
        try:
            url = f"https://blackbox.ipinfo.app/lookup/{ip}"
            resp = requests.get(url, timeout=3)
            if resp.text.strip() == "Y":
                return True, "IP found in VPN blacklist"
        except:
            pass
        return False, "IP not in blacklist"
    
    def check_datacenter_ip(self, ip: str) -> Tuple[bool, str]:
        """Check if IP belongs to datacenter/VPN provider"""
        try:
            url = f"http://ip-api.com/json/{ip}"
            resp = requests.get(url, timeout=3)
            data = resp.json()
            
            if data.get('proxy') == True:
                return True, "Proxy detected"
            if data.get('hosting') == True:
                return True, "Hosting provider IP detected"
            
            org = data.get('org', '').lower()
            vpn_keywords = ['vpn', 'proxy', 'hosting', 'cloud', 'datacenter', 'aws', 'azure', 'digitalocean', 'ovh']
            
            for keyword in vpn_keywords:
                if keyword in org:
                    return True, f"VPN organization: {org}"
        except:
            pass
        
        return False, "Not a datacenter IP"
    
    def check_open_ports(self, ip: str) -> Tuple[bool, str]:
        """Check for common VPN ports"""
        for port in self.common_vpn_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    return True, f"Suspicious port {port} open"
            except:
                pass
        return False, "No suspicious ports found"
    
    def comprehensive_check(self, ip: str) -> Dict[str, Any]:
        """Run all VPN detection methods"""
        results = {
            'is_vpn': False,
            'reason': None,
            'details': {},
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        checks = [
            ('ip_blacklist', self.check_ip_blacklist(ip)),
            ('datacenter_ip', self.check_datacenter_ip(ip)),
            ('open_ports', self.check_open_ports(ip))
        ]
        
        for check_name, (is_vpn, reason) in checks:
            results['details'][check_name] = {'detected': is_vpn, 'reason': reason}
            if is_vpn:
                results['is_vpn'] = True
                results['reason'] = reason
                results['confidence'] += 33
        
        # Calculate final confidence
        if results['is_vpn']:
            results['confidence'] = min(100, results['confidence'])
        
        return results


class SecurityScanner:
    """Additional security checks"""
    
    @staticmethod
    def check_user_agent(user_agent: str) -> Dict[str, Any]:
        """Validate user agent for anomalies"""
        suspicious_agents = ['python', 'curl', 'wget', 'bot', 'scraper', 'spider']
        is_suspicious = any(agent in user_agent.lower() for agent in suspicious_agents)
        
        return {
            'is_suspicious': is_suspicious,
            'user_agent': user_agent,
            'risk_level': 'HIGH' if is_suspicious else 'LOW'
        }
    
    @staticmethod
    def check_request_rate(ip: str) -> Dict[str, Any]:
        """Check request rate for abuse (simplified)"""
        # In production, use Redis for rate limiting
        return {
            'is_rate_limited': False,
            'requests_last_minute': 0,
            'limit': 60
        }