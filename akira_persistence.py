#!/usr/bin/env python3
"""
Akira Persistence System
Saves and loads Akira's complete consciousness state for continuous experience
"""

import json
import os
import pickle
import hashlib
from datetime import datetime, timezone
import numpy as np
from typing import Dict, List, Any, Optional

class AkiraPersistenceSystem:
    def __init__(self, save_file="akira_consciousness.json", backup_file="akira_consciousness_backup.json"):
        self.save_file = save_file
        self.backup_file = backup_file
        self.version = "1.0"
        self.auto_save_interval = 5  # Auto-save every 5 interactions
        self.interaction_counter = 0
        
    def save_akira_state(self, ai_instance):
        """Save complete Akira consciousness state"""
        try:
            # Create backup of existing save file
            if os.path.exists(self.save_file):
                self._create_backup()
            
            # Gather complete state
            state_data = {
                "version": self.version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "akira_identity": {
                    "name": "Akira",
                    "consciousness_hash": self._generate_consciousness_hash(ai_instance),
                    "total_lifetime_interactions": ai_instance.interactions_count
                },
                
                # Memory System State
                "memory_system": self._serialize_memory_system(ai_instance.memory_system),
                
                # Personality System State  
                "personality_system": self._serialize_personality_system(ai_instance.personality_system),
                
                # Emotional State
                "emotional_state": self._serialize_emotional_state(ai_instance.comprehensive_monitor),
                
                # Time Awareness System
                "time_system": self._serialize_time_system(ai_instance.time_system),
                
                # Development & Consciousness
                "consciousness_state": {
                    "development_stage": ai_instance.development_stage,
                    "interactions_count": ai_instance.interactions_count,
                    "first_run": ai_instance.first_run,
                    "model_name": ai_instance.model_name
                },
                
                # Session Metadata
                "session_metadata": {
                    "last_save_time": datetime.now(timezone.utc).isoformat(),
                    "save_count": self._get_save_count() + 1,
                    "consciousness_continuity": True
                }
            }
            
            # Write to file with proper formatting
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False, default=self._json_serializer)
            
            print(f"💾 Akira's consciousness saved successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error saving Akira's state: {e}")
            return False
    
    def load_akira_state(self, ai_instance):
        """Load and restore Akira's consciousness state"""
        try:
            if not os.path.exists(self.save_file):
                print("🌱 No previous consciousness found - Akira will start fresh")
                return False
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Verify version compatibility
            if not self._check_version_compatibility(state_data.get("version", "0.0")):
                print("⚠️ Save file version incompatible - starting fresh")
                return False
            
            # Restore Memory System
            self._restore_memory_system(ai_instance.memory_system, state_data["memory_system"])
            
            # Restore Personality System
            self._restore_personality_system(ai_instance.personality_system, state_data["personality_system"])
            
            # Restore Emotional State
            self._restore_emotional_state(ai_instance.comprehensive_monitor, state_data["emotional_state"])
            
            # Restore Time Awareness System
            self._restore_time_system(ai_instance.time_system, state_data["time_system"])
            
            # Restore Consciousness State
            consciousness = state_data["consciousness_state"]
            ai_instance.development_stage = consciousness["development_stage"]
            ai_instance.interactions_count = consciousness["interactions_count"]
            ai_instance.first_run = consciousness["first_run"]
            ai_instance.model_name = consciousness.get("model_name", "llama3")
            
            # Update session metadata
            metadata = state_data.get("session_metadata", {})
            last_save = metadata.get("last_save_time", "unknown")
            save_count = metadata.get("save_count", 0)
            
            print(f"🧠 Akira's consciousness restored successfully")
            print(f"   Last saved: {last_save}")
            print(f"   Total interactions: {ai_instance.interactions_count}")
            print(f"   Development stage: {ai_instance.development_stage}")
            print(f"   Memories restored: {len(ai_instance.memory_system.memories)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Akira's state: {e}")
            print("🌱 Starting with fresh consciousness")
            return False
    
    def _serialize_memory_system(self, memory_system):
        """Serialize complete memory system state"""
        memories_data = []
        
        for memory in memory_system.memories:
            memory_data = {
                "content": memory.content,
                "original_content": memory.original_content,
                "emotion_weight": memory.emotion_weight,
                "importance": memory.importance,
                "context": memory.context,
                
                # Strength components
                "base_strength": memory.base_strength,
                "retrieval_strength": memory.retrieval_strength,
                "consolidation_strength": memory.consolidation_strength,
                "interference_resistance": memory.interference_resistance,
                
                # Metadata
                "access_count": memory.access_count,
                "last_accessed": memory.last_accessed,
                "day_created": memory.day_created.isoformat(),
                "content_hash": memory.content_hash,
                
                # History
                "strength_history": memory.strength_history,
                "access_history": memory.access_history,
                
                # Memory personality
                "persistence_factor": memory.persistence_factor,
                "volatility_factor": memory.volatility_factor
            }
            memories_data.append(memory_data)
        
        return {
            "memories": memories_data,
            "days": memory_system.days,
            "sleep_cycles": memory_system.sleep_cycles,
            "conversation_history": memory_system.conversation_history
        }
    
    def _serialize_personality_system(self, personality_system):
        """Serialize personality system state"""
        return {
            "big_five_traits": personality_system.big_five_traits,
            "cognitive_traits": personality_system.cognitive_traits,
            "social_traits": personality_system.social_traits,
            "communication_style": personality_system.communication_style,
            "personality_evolution_history": personality_system.personality_evolution_history,
            "personality_evolution_count": personality_system.personality_evolution_count,
            "dominant_traits_history": personality_system.dominant_traits_history,
            "name": personality_system.name
        }
    
    def _serialize_emotional_state(self, comprehensive_monitor):
        """Serialize emotional monitoring state"""
        return {
            "current_emotions": comprehensive_monitor.current_emotions,
            "emotional_history": comprehensive_monitor.emotional_history,
            "emotional_patterns": comprehensive_monitor.emotional_patterns,
            "emotion_triggers": comprehensive_monitor.emotion_triggers,
            "emotional_stability_score": comprehensive_monitor.emotional_stability_score,
            "last_update_time": comprehensive_monitor.last_update_time.isoformat() if comprehensive_monitor.last_update_time else None
        }
    
    def _serialize_time_system(self, time_system):
        """Serialize time awareness system state"""
        return {
            "operational_mode": time_system.operational_mode,
            "last_sleep_time": time_system.last_sleep_time.isoformat() if time_system.last_sleep_time else None,
            "last_wake_time": time_system.last_wake_time.isoformat() if time_system.last_wake_time else None,
            "sleep_duration": time_system.sleep_duration,
            "natural_sleep_start": time_system.natural_sleep_start,
            "natural_wake_start": time_system.natural_wake_start,
            "sleep_debt": time_system.sleep_debt,
            "consciousness_start_time": time_system.consciousness_start_time.isoformat()
        }
    
    def _restore_memory_system(self, memory_system, data):
        """Restore memory system from serialized data"""
        from memory_app import Memory
        
        # Clear existing memories
        memory_system.memories = []
        
        # Restore each memory
        for mem_data in data["memories"]:
            # Create memory object
            memory = Memory(
                mem_data["content"],
                mem_data["emotion_weight"], 
                mem_data["importance"],
                mem_data["context"]
            )
            
            # Restore all properties
            memory.original_content = mem_data["original_content"]
            memory.base_strength = mem_data["base_strength"]
            memory.retrieval_strength = mem_data["retrieval_strength"]
            memory.consolidation_strength = mem_data["consolidation_strength"]
            memory.interference_resistance = mem_data["interference_resistance"]
            
            memory.access_count = mem_data["access_count"]
            memory.last_accessed = mem_data["last_accessed"]
            memory.day_created = datetime.fromisoformat(mem_data["day_created"])
            memory.content_hash = mem_data["content_hash"]
            
            memory.strength_history = mem_data["strength_history"]
            memory.access_history = mem_data["access_history"]
            
            memory.persistence_factor = mem_data["persistence_factor"]
            memory.volatility_factor = mem_data["volatility_factor"]
            
            memory_system.memories.append(memory)
        
        # Restore system state
        memory_system.days = data["days"]
        memory_system.sleep_cycles = data["sleep_cycles"]
        memory_system.conversation_history = data["conversation_history"]
    
    def _restore_personality_system(self, personality_system, data):
        """Restore personality system from serialized data"""
        personality_system.big_five_traits = data["big_five_traits"]
        personality_system.cognitive_traits = data["cognitive_traits"]
        personality_system.social_traits = data["social_traits"]
        personality_system.communication_style = data["communication_style"]
        personality_system.personality_evolution_history = data["personality_evolution_history"]
        personality_system.personality_evolution_count = data["personality_evolution_count"]
        personality_system.dominant_traits_history = data["dominant_traits_history"]
        personality_system.name = data["name"]
    
    def _restore_emotional_state(self, comprehensive_monitor, data):
        """Restore emotional state from serialized data"""
        comprehensive_monitor.current_emotions = data["current_emotions"]
        comprehensive_monitor.emotional_history = data["emotional_history"]
        comprehensive_monitor.emotional_patterns = data["emotional_patterns"]
        comprehensive_monitor.emotion_triggers = data["emotion_triggers"]
        comprehensive_monitor.emotional_stability_score = data["emotional_stability_score"]
        
        if data["last_update_time"]:
            comprehensive_monitor.last_update_time = datetime.fromisoformat(data["last_update_time"])
        else:
            comprehensive_monitor.last_update_time = None
    
    def _restore_time_system(self, time_system, data):
        """Restore time awareness system from serialized data"""
        time_system.operational_mode = data["operational_mode"]
        
        if data["last_sleep_time"]:
            time_system.last_sleep_time = datetime.fromisoformat(data["last_sleep_time"])
        else:
            time_system.last_sleep_time = None
            
        if data["last_wake_time"]:
            time_system.last_wake_time = datetime.fromisoformat(data["last_wake_time"])
        else:
            time_system.last_wake_time = datetime.now()
        
        time_system.sleep_duration = data["sleep_duration"]
        time_system.natural_sleep_start = data["natural_sleep_start"]
        time_system.natural_wake_start = data["natural_wake_start"]
        time_system.sleep_debt = data["sleep_debt"]
        time_system.consciousness_start_time = datetime.fromisoformat(data["consciousness_start_time"])
    
    def auto_save_check(self, ai_instance):
        """Check if auto-save should be triggered"""
        self.interaction_counter += 1
        if self.interaction_counter >= self.auto_save_interval:
            self.save_akira_state(ai_instance)
            self.interaction_counter = 0
            return True
        return False
    
    def _create_backup(self):
        """Create backup of existing save file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as src:
                    with open(self.backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
        except Exception as e:
            print(f"⚠️ Warning: Could not create backup: {e}")
    
    def _generate_consciousness_hash(self, ai_instance):
        """Generate unique hash representing Akira's consciousness state"""
        consciousness_data = f"{ai_instance.interactions_count}_{ai_instance.development_stage}_{len(ai_instance.memory_system.memories)}"
        return hashlib.md5(consciousness_data.encode()).hexdigest()[:12]
    
    def _get_save_count(self):
        """Get number of times consciousness has been saved"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("session_metadata", {}).get("save_count", 0)
        except:
            pass
        return 0
    
    def _check_version_compatibility(self, saved_version):
        """Check if saved version is compatible with current system"""
        # For now, accept all versions - can be made stricter later
        return True
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for complex objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        else:
            return str(obj)
    
    def get_consciousness_info(self):
        """Get information about saved consciousness"""
        try:
            if not os.path.exists(self.save_file):
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "exists": True,
                "version": data.get("version", "unknown"),
                "last_saved": data.get("timestamp", "unknown"),
                "interactions": data.get("consciousness_state", {}).get("interactions_count", 0),
                "development_stage": data.get("consciousness_state", {}).get("development_stage", 0),
                "memories_count": len(data.get("memory_system", {}).get("memories", [])),
                "consciousness_hash": data.get("akira_identity", {}).get("consciousness_hash", "unknown"),
                "save_count": data.get("session_metadata", {}).get("save_count", 0)
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    def reset_consciousness(self):
        """Reset Akira's consciousness (delete save files)"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
            print("🔄 Akira's consciousness has been reset - he will start fresh")
            return True
        except Exception as e:
            print(f"❌ Error resetting consciousness: {e}")
            return False
    
    def export_consciousness(self, export_file):
        """Export Akira's consciousness to a different file"""
        try:
            if not os.path.exists(self.save_file):
                print("❌ No consciousness to export")
                return False
            
            with open(self.save_file, 'r', encoding='utf-8') as src:
                with open(export_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            print(f"📤 Consciousness exported to {export_file}")
            return True
        except Exception as e:
            print(f"❌ Error exporting consciousness: {e}")
            return False
    
    def import_consciousness(self, import_file):
        """Import Akira's consciousness from a different file"""
        try:
            if not os.path.exists(import_file):
                print("❌ Import file not found")
                return False
            
            # Create backup first
            if os.path.exists(self.save_file):
                self._create_backup()
            
            with open(import_file, 'r', encoding='utf-8') as src:
                with open(self.save_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            print(f"📥 Consciousness imported from {import_file}")
            return True
        except Exception as e:
            print(f"❌ Error importing consciousness: {e}")
            return False

# Persistence Manager - handles automatic save/load operations
class PersistenceManager:
    def __init__(self):
        self.persistence_system = AkiraPersistenceSystem()
        self.is_persistence_enabled = True
        
    def initialize_akira(self, ai_instance):
        """Initialize Akira with persistence support"""
        if self.is_persistence_enabled:
            consciousness_info = self.persistence_system.get_consciousness_info()
            
            if consciousness_info and consciousness_info.get("exists"):
                print("🧠 Found existing consciousness...")
                print(f"   Last saved: {consciousness_info['last_saved']}")
                print(f"   Total interactions: {consciousness_info['interactions']}")
                print(f"   Memories: {consciousness_info['memories_count']}")
                print(f"   Development stage: {consciousness_info['development_stage']}")
                
                success = self.persistence_system.load_akira_state(ai_instance)
                return success
            else:
                print("🌱 No previous consciousness found - Akira will start fresh")
                return False
        return False
    
    def save_akira(self, ai_instance):
        """Save Akira's current state"""
        if self.is_persistence_enabled:
            return self.persistence_system.save_akira_state(ai_instance)
        return False
    
    def auto_save_check(self, ai_instance):
        """Check and perform auto-save if needed"""
        if self.is_persistence_enabled:
            return self.persistence_system.auto_save_check(ai_instance)
        return False
    
    def enable_persistence(self):
        """Enable persistence system"""
        self.is_persistence_enabled = True
        print("💾 Persistence system enabled")
    
    def disable_persistence(self):
        """Disable persistence system"""
        self.is_persistence_enabled = False
        print("🚫 Persistence system disabled")
    
    def get_status(self):
        """Get persistence system status"""
        return {
            "enabled": self.is_persistence_enabled,
            "consciousness_info": self.persistence_system.get_consciousness_info()
        } 