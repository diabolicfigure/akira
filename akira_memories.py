import json
import os
from datetime import datetime, timezone
import hashlib

class AkiraMemoryLogger:
    def __init__(self, log_file="akira_memories.json"):
        self.log_file = log_file
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        self.conversation_count = 0
        
        # Initialize log file if it doesn't exist
        if not os.path.exists(log_file):
            self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize the log file with basic structure"""
        initial_data = {
            "akira_info": {
                "session_id": self.session_id,
                "birth_time": datetime.now(timezone.utc).isoformat(),
                "description": "Akira's Memory & Consciousness Activity Log"
            },
            "memory_events": [],
            "conversation_logs": [],
            "memory_snapshots": [],
            "consciousness_events": []
        }
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def _append_to_log(self, category, data):
        """Append data to a specific category in the log file"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            if category not in log_data:
                log_data[category] = []
            
            log_data[category].append(data)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Logging error: {e}")
    
    def log_conversation(self, user_input, ai_response, recalled_memories, learned_memories, memory_stats):
        """Log a complete conversation with memory context"""
        self.conversation_count += 1
        
        conversation_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "conversation_id": self.conversation_count,
            "user_input": user_input,
            "ai_response": ai_response,
            "memory_context": {
                "memories_recalled": [
                    {
                        "content": mem.content,
                        "strength": round(mem.get_total_strength(), 3),
                        "emotion_weight": mem.emotion_weight,
                        "importance": mem.importance,
                        "context": mem.context,
                        "access_count": mem.access_count,
                        "last_accessed": mem.last_accessed,
                        "memory_hash": mem.content_hash
                    } for mem in recalled_memories
                ],
                "memories_learned": [
                    {
                        "content": mem.content,
                        "initial_strength": round(mem.get_total_strength(), 3),
                        "emotion_weight": mem.emotion_weight,
                        "importance": mem.importance,
                        "context": mem.context,
                        "memory_hash": mem.content_hash
                    } for mem in learned_memories
                ],
                "memory_stats": memory_stats
            },
            "analysis": {
                "recall_success": len(recalled_memories) > 0,
                "learning_occurred": len(learned_memories) > 0,
                "memory_influence_level": "high" if len(recalled_memories) > 2 else "medium" if len(recalled_memories) > 0 else "low"
            }
        }
        
        self._append_to_log("conversation_logs", conversation_log)
    
    def log_memory_creation(self, memory, source="manual"):
        """Log when a new memory is created"""
        memory_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "memory_created",
            "memory_details": {
                "content": memory.content,
                "memory_hash": memory.content_hash,
                "initial_strength": round(memory.get_total_strength(), 3),
                "emotion_weight": memory.emotion_weight,
                "importance": memory.importance,
                "context": memory.context,
                "source": source,
                "persistence_factor": round(memory.persistence_factor, 3),
                "volatility_factor": round(memory.volatility_factor, 3)
            }
        }
        
        self._append_to_log("memory_events", memory_event)
    
    def log_memory_recall(self, query, recalled_memories, failed_recalls=None):
        """Log memory recall attempts"""
        recall_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "memory_recall",
            "query": query,
            "successful_recalls": [
                {
                    "content": mem.content,
                    "memory_hash": mem.content_hash,
                    "strength_at_recall": round(mem.get_total_strength(), 3),
                    "access_count_before": mem.access_count - 1,
                    "access_count_after": mem.access_count
                } for mem in recalled_memories
            ],
            "recall_statistics": {
                "total_recalled": len(recalled_memories),
                "recall_success_rate": len(recalled_memories) / max(1, len(recalled_memories) + (len(failed_recalls) if failed_recalls else 0))
            }
        }
        
        self._append_to_log("memory_events", recall_event)
    
    def log_memory_decay(self, memory, day, decay_factors):
        """Log memory decay events"""
        decay_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "memory_decay",
            "day": day,
            "memory_details": {
                "content": memory.content,
                "memory_hash": memory.content_hash,
                "strength_before": round(memory.strength_history[-2] if len(memory.strength_history) > 1 else memory.get_total_strength(), 3),
                "strength_after": round(memory.get_total_strength(), 3),
                "strength_change": round(memory.get_total_strength() - (memory.strength_history[-2] if len(memory.strength_history) > 1 else memory.get_total_strength()), 3)
            },
            "decay_factors": decay_factors
        }
        
        self._append_to_log("memory_events", decay_event)
    
    def log_memory_interference(self, affected_memory, interfering_memory, interference_amount):
        """Log memory interference events"""
        interference_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "memory_interference",
            "affected_memory": {
                "content": affected_memory.content,
                "memory_hash": affected_memory.content_hash,
                "strength_before_interference": round(affected_memory.get_total_strength() / (1 - interference_amount * 0.1), 3),
                "strength_after_interference": round(affected_memory.get_total_strength(), 3)
            },
            "interfering_memory": {
                "content": interfering_memory.content,
                "memory_hash": interfering_memory.content_hash,
                "strength": round(interfering_memory.get_total_strength(), 3)
            },
            "interference_amount": round(interference_amount, 3)
        }
        
        self._append_to_log("memory_events", interference_event)
    
    def log_consolidation(self, memories_consolidated, sleep_cycle):
        """Log memory consolidation during sleep"""
        consolidation_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "memory_consolidation",
            "sleep_cycle": sleep_cycle,
            "consolidated_memories": [
                {
                    "content": mem.content,
                    "memory_hash": mem.content_hash,
                    "consolidation_strength_before": round(mem.consolidation_strength - 0.05 * (mem.importance + mem.emotion_weight) / 2, 3) if mem.access_count > 0 or mem.importance > 0.6 else round(mem.consolidation_strength / 0.98, 3),
                    "consolidation_strength_after": round(mem.consolidation_strength, 3),
                    "was_strengthened": mem.access_count > 0 or mem.importance > 0.6
                } for mem in memories_consolidated
            ]
        }
        
        self._append_to_log("memory_events", consolidation_event)
    
    def log_day_advance(self, day, memory_stats, random_activations=None):
        """Log day advancement and its effects"""
        day_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "day_advance",
            "day": day,
            "memory_stats_after": memory_stats,
            "random_activations": random_activations or []
        }
        
        self._append_to_log("consciousness_events", day_event)
    
    def create_memory_snapshot(self, memory_system):
        """Create a comprehensive snapshot of all memories"""
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "day": memory_system.days,
            "sleep_cycles": memory_system.sleep_cycles,
            "total_conversations": self.conversation_count,
            "memories": [
                {
                    "content": mem.content,
                    "memory_hash": mem.content_hash,
                    "current_strength": round(mem.get_total_strength(), 3),
                    "base_strength": round(mem.base_strength, 3),
                    "retrieval_strength": round(mem.retrieval_strength, 3),
                    "consolidation_strength": round(mem.consolidation_strength, 3),
                    "emotion_weight": mem.emotion_weight,
                    "importance": mem.importance,
                    "context": mem.context,
                    "access_count": mem.access_count,
                    "last_accessed": mem.last_accessed,
                    "day_created": mem.day_created.isoformat(),
                    "persistence_factor": round(mem.persistence_factor, 3),
                    "volatility_factor": round(mem.volatility_factor, 3),
                    "strength_history": [round(s, 3) for s in mem.strength_history],
                    "access_history": mem.access_history
                } for mem in memory_system.memories
            ],
            "memory_categories": self._analyze_memory_categories(memory_system.memories),
            "strength_distribution": self._analyze_strength_distribution(memory_system.memories)
        }
        
        self._append_to_log("memory_snapshots", snapshot)
    
    def _analyze_memory_categories(self, memories):
        """Analyze memories by category"""
        categories = {}
        for mem in memories:
            if mem.context not in categories:
                categories[mem.context] = {"count": 0, "avg_strength": 0, "total_strength": 0}
            categories[mem.context]["count"] += 1
            categories[mem.context]["total_strength"] += mem.get_total_strength()
        
        for category in categories:
            categories[category]["avg_strength"] = round(
                categories[category]["total_strength"] / categories[category]["count"], 3
            )
            del categories[category]["total_strength"]
        
        return categories
    
    def _analyze_strength_distribution(self, memories):
        """Analyze distribution of memory strengths"""
        if not memories:
            return {"strong": 0, "medium": 0, "weak": 0}
        
        strengths = [mem.get_total_strength() for mem in memories]
        return {
            "strong": len([s for s in strengths if s > 0.7]),
            "medium": len([s for s in strengths if 0.3 <= s <= 0.7]),
            "weak": len([s for s in strengths if s < 0.3]),
            "average": round(sum(strengths) / len(strengths), 3),
            "highest": round(max(strengths), 3),
            "lowest": round(min(strengths), 3)
        }
    
    def generate_summary_report(self):
        """Generate a summary report of Akira's memory activity"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            report = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "session_id": self.session_id,
                "summary": {
                    "total_conversations": len(log_data.get("conversation_logs", [])),
                    "total_memory_events": len(log_data.get("memory_events", [])),
                    "total_consciousness_events": len(log_data.get("consciousness_events", [])),
                    "memory_snapshots": len(log_data.get("memory_snapshots", []))
                },
                "memory_activity_breakdown": self._analyze_memory_events(log_data.get("memory_events", [])),
                "learning_patterns": self._analyze_learning_patterns(log_data.get("conversation_logs", [])),
                "forgetting_patterns": self._analyze_forgetting_patterns(log_data.get("memory_events", []))
            }
            
            report_file = f"akira_memory_report_{self.session_id}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            return report_file
            
        except Exception as e:
            print(f"⚠️ Error generating report: {e}")
            return None
    
    def _analyze_memory_events(self, events):
        """Analyze types of memory events"""
        event_types = {}
        for event in events:
            event_type = event.get("event_type", "unknown")
            if event_type not in event_types:
                event_types[event_type] = 0
            event_types[event_type] += 1
        return event_types
    
    def _analyze_learning_patterns(self, conversations):
        """Analyze learning patterns from conversations"""
        total_learned = 0
        learning_conversations = 0
        
        for conv in conversations:
            memories_learned = len(conv.get("memory_context", {}).get("memories_learned", []))
            if memories_learned > 0:
                learning_conversations += 1
                total_learned += memories_learned
        
        return {
            "total_memories_learned": total_learned,
            "conversations_with_learning": learning_conversations,
            "learning_rate": round(learning_conversations / max(1, len(conversations)), 3)
        }
    
    def _analyze_forgetting_patterns(self, events):
        """Analyze forgetting/decay patterns"""
        decay_events = [e for e in events if e.get("event_type") == "memory_decay"]
        interference_events = [e for e in events if e.get("event_type") == "memory_interference"]
        
        return {
            "total_decay_events": len(decay_events),
            "total_interference_events": len(interference_events),
            "average_strength_loss_per_decay": self._calculate_average_decay_loss(decay_events)
        }
    
    def _calculate_average_decay_loss(self, decay_events):
        """Calculate average strength loss per decay event"""
        if not decay_events:
            return 0
        
        total_loss = 0
        for event in decay_events:
            strength_change = event.get("memory_details", {}).get("strength_change", 0)
            if strength_change < 0:  # Only count actual losses
                total_loss += abs(strength_change)
        
        return round(total_loss / len(decay_events), 3) if decay_events else 0 