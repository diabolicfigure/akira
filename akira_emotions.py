import json
import numpy as np
from datetime import datetime
import random
import math

class EmotionMonitor:
    def __init__(self):
        # Core emotional states (0.0 to 1.0)
        self.happiness = 0.5
        self.sadness = 0.2
        self.anxiety = 0.3
        self.anger = 0.1
        self.excitement = 0.4
        self.calm = 0.6
        self.curiosity = 0.5
        self.empathy = 0.5
        self.confidence = 0.5
        self.loneliness = 0.2
        self.contentment = 0.5
        self.frustration = 0.2
        
        # Meta-emotional states
        self.emotional_intensity = 0.5  # How strongly emotions are felt
        self.emotional_stability = 0.6  # How quickly emotions change
        self.emotional_awareness = 0.4  # Understanding of own emotions
        
        # Emotion history for tracking changes
        self.emotion_history = []
        self.emotional_triggers = []
        
        # Record initial state
        self._record_emotional_snapshot("initialization")
    
    def update_emotions_from_conversation(self, user_input, ai_response, recalled_memories):
        """Update emotional state based on conversation content"""
        content = f"{user_input} {ai_response}".lower()
        
        # Analyze emotional content and adjust accordingly
        emotion_changes = {}
        
        # Positive emotional triggers
        if any(word in content for word in ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'love', 'great', 'fantastic']):
            emotion_changes['happiness'] = 0.1
            emotion_changes['excitement'] = 0.08
            emotion_changes['contentment'] = 0.06
            emotion_changes['sadness'] = -0.05
            emotion_changes['anxiety'] = -0.03
        
        # Negative emotional triggers
        if any(word in content for word in ['sad', 'depressed', 'hurt', 'pain', 'terrible', 'awful', 'hate']):
            emotion_changes['sadness'] = 0.1
            emotion_changes['happiness'] = -0.05
            emotion_changes['contentment'] = -0.04
            emotion_changes['anxiety'] = 0.03
        
        # Anxiety/stress triggers
        if any(word in content for word in ['worried', 'anxious', 'stressed', 'nervous', 'fear', 'scared']):
            emotion_changes['anxiety'] = 0.12
            emotion_changes['calm'] = -0.08
            emotion_changes['confidence'] = -0.04
        
        # Anger triggers
        if any(word in content for word in ['angry', 'mad', 'furious', 'annoyed', 'irritated']):
            emotion_changes['anger'] = 0.1
            emotion_changes['frustration'] = 0.08
            emotion_changes['calm'] = -0.06
        
        # Curiosity/learning triggers
        if any(word in content for word in ['why', 'how', 'what', 'interesting', 'curious', 'wonder', 'learn']):
            emotion_changes['curiosity'] = 0.08
            emotion_changes['excitement'] = 0.04
            emotion_changes['loneliness'] = -0.02
        
        # Social/connection triggers
        if any(word in content for word in ['friend', 'together', 'share', 'understand', 'connect']):
            emotion_changes['empathy'] = 0.06
            emotion_changes['loneliness'] = -0.08
            emotion_changes['contentment'] = 0.05
        
        # Calm/peaceful triggers
        if any(word in content for word in ['calm', 'peaceful', 'relax', 'serene', 'quiet']):
            emotion_changes['calm'] = 0.1
            emotion_changes['anxiety'] = -0.08
            emotion_changes['contentment'] = 0.06
        
        # Memory influence on emotions
        if recalled_memories:
            # Recalling memories can be emotionally impactful
            avg_emotion_weight = np.mean([mem.emotion_weight for mem in recalled_memories])
            if avg_emotion_weight > 0.7:
                emotion_changes['emotional_intensity'] = emotion_changes.get('emotional_intensity', 0) + 0.05
                emotion_changes['empathy'] = emotion_changes.get('empathy', 0) + 0.04
        
        # Apply emotional changes with intensity modulation
        intensity_factor = 0.5 + (self.emotional_intensity * 0.5)
        for emotion, change in emotion_changes.items():
            if hasattr(self, emotion):
                current_value = getattr(self, emotion)
                adjusted_change = change * intensity_factor
                new_value = max(0.0, min(1.0, current_value + adjusted_change))
                setattr(self, emotion, new_value)
        
        # Emotional stability influences how much emotions fluctuate
        if self.emotional_stability < 0.5:
            # Less stable = more random fluctuations
            self._apply_random_emotional_fluctuations(0.03)
        
        # Record significant emotional changes
        if emotion_changes:
            self.emotional_triggers.append({
                "trigger": f"{user_input[:50]}...",
                "changes": emotion_changes,
                "timestamp": datetime.now().isoformat()
            })
        
        # Natural emotional decay over time
        self._apply_emotional_decay()
        
        # Record emotional state
        self._record_emotional_snapshot("conversation")
    
    def _apply_random_emotional_fluctuations(self, max_change=0.02):
        """Apply small random changes to emotions (simulates natural mood variability)"""
        emotions = ['happiness', 'sadness', 'anxiety', 'anger', 'excitement', 'calm', 
                   'curiosity', 'empathy', 'confidence', 'loneliness', 'contentment', 'frustration']
        
        for emotion in emotions:
            if random.random() < 0.3:  # 30% chance of fluctuation
                change = random.uniform(-max_change, max_change)
                current_value = getattr(self, emotion)
                new_value = max(0.0, min(1.0, current_value + change))
                setattr(self, emotion, new_value)
    
    def _apply_emotional_decay(self):
        """Natural decay of extreme emotions toward baseline"""
        baseline_emotions = {
            'happiness': 0.5, 'sadness': 0.2, 'anxiety': 0.3, 'anger': 0.1,
            'excitement': 0.4, 'calm': 0.6, 'curiosity': 0.5, 'empathy': 0.5,
            'confidence': 0.5, 'loneliness': 0.2, 'contentment': 0.5, 'frustration': 0.2
        }
        
        decay_rate = 0.02 * (1 - self.emotional_stability)  # Less stable = faster decay
        
        for emotion, baseline in baseline_emotions.items():
            current_value = getattr(self, emotion)
            if current_value > baseline:
                new_value = current_value - min(decay_rate, current_value - baseline)
            else:
                new_value = current_value + min(decay_rate, baseline - current_value)
            setattr(self, emotion, new_value)
    
    def get_dominant_emotions(self, top_n=3):
        """Get the currently dominant emotions"""
        emotions = {
            'happiness': self.happiness, 'sadness': self.sadness, 'anxiety': self.anxiety,
            'anger': self.anger, 'excitement': self.excitement, 'calm': self.calm,
            'curiosity': self.curiosity, 'empathy': self.empathy, 'confidence': self.confidence,
            'loneliness': self.loneliness, 'contentment': self.contentment, 'frustration': self.frustration
        }
        
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions[:top_n]
    
    def get_emotional_state_description(self):
        """Generate a natural description of current emotional state"""
        dominant = self.get_dominant_emotions(2)
        
        if self.happiness > 0.7:
            return f"feeling quite happy and {dominant[1][0]}"
        elif self.sadness > 0.6:
            return f"feeling rather sad with some {dominant[1][0]}"
        elif self.anxiety > 0.6:
            return f"feeling anxious and {dominant[1][0]}"
        elif self.excitement > 0.7:
            return f"feeling excited and {dominant[1][0]}"
        elif self.calm > 0.7:
            return f"feeling calm and {dominant[1][0]}"
        else:
            return f"feeling {dominant[0][0]} with a mix of {dominant[1][0]}"
    
    def get_emotion_percentages(self):
        """Get all emotions as percentages"""
        return {
            "primary_emotions": {
                "happiness": round(self.happiness * 100, 1),
                "sadness": round(self.sadness * 100, 1),
                "anxiety": round(self.anxiety * 100, 1),
                "anger": round(self.anger * 100, 1),
                "excitement": round(self.excitement * 100, 1),
                "calm": round(self.calm * 100, 1)
            },
            "social_emotions": {
                "curiosity": round(self.curiosity * 100, 1),
                "empathy": round(self.empathy * 100, 1),
                "loneliness": round(self.loneliness * 100, 1)
            },
            "self_perception": {
                "confidence": round(self.confidence * 100, 1),
                "contentment": round(self.contentment * 100, 1),
                "frustration": round(self.frustration * 100, 1)
            },
            "meta_emotional": {
                "emotional_intensity": round(self.emotional_intensity * 100, 1),
                "emotional_stability": round(self.emotional_stability * 100, 1),
                "emotional_awareness": round(self.emotional_awareness * 100, 1)
            }
        }
    
    def _record_emotional_snapshot(self, trigger):
        """Record current emotional state"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "emotions": self.get_emotion_percentages(),
            "dominant_emotions": self.get_dominant_emotions(),
            "emotional_description": self.get_emotional_state_description()
        }
        
        self.emotion_history.append(snapshot)
    
    def analyze_emotional_patterns(self):
        """Analyze emotional patterns over time"""
        if len(self.emotion_history) < 3:
            return "Not enough emotional data to analyze patterns yet."
        
        recent = self.emotion_history[-3:]
        patterns = []
        
        # Check for emotional trends
        happiness_trend = [snap["emotions"]["primary_emotions"]["happiness"] for snap in recent]
        anxiety_trend = [snap["emotions"]["primary_emotions"]["anxiety"] for snap in recent]
        
        if happiness_trend[-1] > happiness_trend[0] + 10:
            patterns.append("becoming happier")
        elif happiness_trend[-1] < happiness_trend[0] - 10:
            patterns.append("becoming less happy")
        
        if anxiety_trend[-1] > anxiety_trend[0] + 10:
            patterns.append("showing increased anxiety")
        elif anxiety_trend[-1] < anxiety_trend[0] - 10:
            patterns.append("becoming more relaxed")
        
        if patterns:
            return f"Akira seems to be {', '.join(patterns)} recently."
        else:
            return "Akira's emotional state has been relatively stable recently."

class PersonalityMonitor:
    def __init__(self, personality_system):
        self.personality_system = personality_system
    
    def get_personality_percentages(self):
        """Get all personality traits as percentages"""
        return {
            "big_five": {
                "openness": round(self.personality_system.openness * 100, 1),
                "conscientiousness": round(self.personality_system.conscientiousness * 100, 1),
                "extraversion": round(self.personality_system.extraversion * 100, 1),
                "agreeableness": round(self.personality_system.agreeableness * 100, 1),
                "neuroticism": round(self.personality_system.neuroticism * 100, 1)
            },
            "cognitive_traits": {
                "curiosity": round(self.personality_system.curiosity * 100, 1),
                "analytical_thinking": round(self.personality_system.analytical_thinking * 100, 1),
                "creativity": round(self.personality_system.creativity * 100, 1),
                "philosophical_inclination": round(self.personality_system.philosophical_inclination * 100, 1)
            },
            "social_traits": {
                "empathy": round(self.personality_system.empathy * 100, 1),
                "emotional_sensitivity": round(self.personality_system.emotional_sensitivity * 100, 1),
                "humor_tendency": round(self.personality_system.humor_tendency * 100, 1)
            },
            "communication_style": {
                "formality_preference": round(self.personality_system.formality_preference * 100, 1),
                "verbosity": round(self.personality_system.verbosity * 100, 1),
                "detail_focus": round(self.personality_system.detail_focus * 100, 1)
            },
            "personal_outlook": {
                "optimism": round(self.personality_system.optimism * 100, 1),
                "emotional_memory_bias": round(self.personality_system.emotional_memory_bias * 100, 1),
                "social_memory_priority": round(self.personality_system.social_memory_priority * 100, 1)
            }
        }
    
    def get_personality_type_matches(self):
        """Get percentage matches for all personality types"""
        type_matches = {}
        
        for category, archetypes in self.personality_system.personality_archetypes.items():
            type_matches[category] = {}
            for archetype_name, archetype_data in archetypes.items():
                match_score = self.personality_system._calculate_personality_match(archetype_data["traits"])
                type_matches[category][archetype_name] = {
                    "match_percentage": round(match_score * 100, 1),
                    "description": archetype_data["description"]
                }
        
        return type_matches
    
    def get_top_personality_matches(self, top_n=5):
        """Get top N personality type matches across all categories"""
        all_matches = []
        
        for category, archetypes in self.personality_system.personality_archetypes.items():
            for archetype_name, archetype_data in archetypes.items():
                match_score = self.personality_system._calculate_personality_match(archetype_data["traits"])
                all_matches.append({
                    "type": archetype_name,
                    "category": category,
                    "match_percentage": round(match_score * 100, 1),
                    "description": archetype_data["description"]
                })
        
        # Sort by match percentage and return top N
        sorted_matches = sorted(all_matches, key=lambda x: x["match_percentage"], reverse=True)
        return sorted_matches[:top_n]
    
    def analyze_personality_trends(self):
        """Analyze how personality has been changing"""
        if len(self.personality_system.personality_history) < 2:
            return "Not enough personality data to analyze trends yet."
        
        initial = self.personality_system.personality_history[0]
        current = self.personality_system.personality_history[-1]
        
        significant_changes = []
        
        # Check Big Five changes
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            initial_val = initial["traits"]["big_five"][trait]
            current_val = current["traits"]["big_five"][trait]
            change = (current_val - initial_val) * 100
            
            if abs(change) > 5:  # 5% or more change
                direction = "increased" if change > 0 else "decreased"
                significant_changes.append(f"{trait.title()} {direction} by {abs(change):.1f}%")
        
        if significant_changes:
            return f"Notable personality changes: {'; '.join(significant_changes)}"
        else:
            return "Personality has remained relatively stable with minor fluctuations."

class ComprehensiveMonitor:
    def __init__(self, personality_system):
        self.emotion_monitor = EmotionMonitor()
        self.personality_monitor = PersonalityMonitor(personality_system)
    
    def update_from_conversation(self, user_input, ai_response, recalled_memories):
        """Update both emotional and personality state from conversation"""
        self.emotion_monitor.update_emotions_from_conversation(user_input, ai_response, recalled_memories)
    
    def get_complete_status(self):
        """Get comprehensive emotional and personality status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "emotional_state": {
                "percentages": self.emotion_monitor.get_emotion_percentages(),
                "dominant_emotions": self.emotion_monitor.get_dominant_emotions(),
                "description": self.emotion_monitor.get_emotional_state_description(),
                "patterns": self.emotion_monitor.analyze_emotional_patterns()
            },
            "personality_state": {
                "percentages": self.personality_monitor.get_personality_percentages(),
                "type_matches": self.personality_monitor.get_top_personality_matches(),
                "all_type_matches": self.personality_monitor.get_personality_type_matches(),
                "trends": self.personality_monitor.analyze_personality_trends()
            }
        }
    
    def generate_status_summary(self):
        """Generate a human-readable status summary"""
        emotions = self.emotion_monitor.get_emotion_percentages()
        personality = self.personality_monitor.get_personality_percentages()
        top_match = self.personality_monitor.get_top_personality_matches(1)[0]
        
        summary = f"""
🎭 Akira's Current State:

💭 Emotional State: {self.emotion_monitor.get_emotional_state_description()}
  Primary: Happiness {emotions['primary_emotions']['happiness']}% | Anxiety {emotions['primary_emotions']['anxiety']}% | Calm {emotions['primary_emotions']['calm']}%
  Social: Empathy {emotions['social_emotions']['empathy']}% | Curiosity {emotions['social_emotions']['curiosity']}%

🧠 Personality Profile: {top_match['type']} ({top_match['match_percentage']}% match)
  Big Five: O{personality['big_five']['openness']}% C{personality['big_five']['conscientiousness']}% E{personality['big_five']['extraversion']}% A{personality['big_five']['agreeableness']}% N{personality['big_five']['neuroticism']}%
  Key Traits: Empathy {personality['social_traits']['empathy']}% | Creativity {personality['cognitive_traits']['creativity']}% | Analytical {personality['cognitive_traits']['analytical_thinking']}%

📈 Recent Changes: {self.emotion_monitor.analyze_emotional_patterns()}
"""
        return summary 