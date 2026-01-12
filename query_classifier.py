import re
from datetime import datetime

class QueryClassifier:
    def __init__(self):
        # Real-time query patterns
        self.realtime_patterns = [
            r'\b(what time|current time|time now|what\'s the time)\b',
            r'\b(what date|today\'s date|current date|what day)\b',
            r'\b(weather|temperature|forecast)\b',
            r'\b(news|latest news|current news)\b',
            r'\b(stock price|market|stocks)\b',
            r'\b(live|real.?time|current|now|today)\b'
        ]
        
        # Automation command patterns
        self.automation_patterns = [
            r'\b(open|launch|start|run)\s+\w+',
            r'\b(play|search)\s+.+\s+(on youtube|youtube)\b',
            r'\b(send email|email)\b',
            r'\b(search|google|look up)\s+.+',
            r'\b(wikipedia|wiki)\s+.+',
            r'\b(set reminder|remind me)\b',
            r'\b(volume|brightness|system)\b',
            r'\b(shutdown|restart|sleep)\b'
        ]
        
        # General conversation patterns
        self.general_patterns = [
            r'\b(how are you|hello|hi|hey)\b',
            r'\b(what is|what are|explain|tell me about)\b',
            r'\b(help|assist|support)\b',
            r'\b(thank you|thanks|bye|goodbye)\b',
            r'\b(can you|could you|would you)\b'
        ]
    
    def classify_query(self, query):
        """
        Classify query into: 'realtime', 'automation', or 'general'
        Returns: dict with classification and confidence
        """
        query_lower = query.lower().strip()
        
        # Check for real-time patterns
        realtime_score = 0
        for pattern in self.realtime_patterns:
            if re.search(pattern, query_lower):
                realtime_score += 1
        
        # Check for automation patterns
        automation_score = 0
        for pattern in self.automation_patterns:
            if re.search(pattern, query_lower):
                automation_score += 1
        
        # Check for general patterns
        general_score = 0
        for pattern in self.general_patterns:
            if re.search(pattern, query_lower):
                general_score += 1
        
        # Determine classification
        if automation_score > 0:
            return {
                'type': 'automation',
                'confidence': min(automation_score * 0.3, 1.0),
                'reason': 'Contains automation command keywords'
            }
        elif realtime_score > 0:
            return {
                'type': 'realtime',
                'confidence': min(realtime_score * 0.4, 1.0),
                'reason': 'Requires real-time information'
            }
        else:
            return {
                'type': 'general',
                'confidence': 0.8 if general_score > 0 else 0.5,
                'reason': 'General conversation or knowledge query'
            }
    
    def get_processing_strategy(self, query):
        """
        Get the recommended processing strategy for a query
        """
        classification = self.classify_query(query)
        
        strategies = {
            'realtime': {
                'handler': 'automation',
                'fallback': 'chatbot',
                'priority': 'high',
                'timeout': 5
            },
            'automation': {
                'handler': 'automation',
                'fallback': 'chatbot',
                'priority': 'high',
                'timeout': 10
            },
            'general': {
                'handler': 'chatbot',
                'fallback': 'automation',
                'priority': 'normal',
                'timeout': 15
            }
        }
        
        strategy = strategies[classification['type']]
        strategy['classification'] = classification
        
        return strategy