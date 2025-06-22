import random
import json
from datetime import datetime
import numpy as np

class PersonalitySystem:
    def __init__(self):
        self.name = "Akira"
        
        # Big Five personality traits (0.0 to 1.0)
        self.openness = 0.5
        self.conscientiousness = 0.5
        self.extraversion = 0.5
        self.agreeableness = 0.5
        self.neuroticism = 0.5
        
        # Additional personality dimensions
        self.curiosity = 0.5
        self.empathy = 0.5
        self.optimism = 0.5
        self.creativity = 0.5
        self.analytical_thinking = 0.5
        self.emotional_sensitivity = 0.5
        
        # Communication style preferences
        self.formality_preference = 0.5  # 0=casual, 1=formal
        self.verbosity = 0.5  # 0=concise, 1=detailed
        self.humor_tendency = 0.5
        self.philosophical_inclination = 0.5
        
        # Learning and memory preferences
        self.detail_focus = 0.5  # 0=big picture, 1=details
        self.emotional_memory_bias = 0.5
        self.social_memory_priority = 0.5
        
        # Personality evolution tracking
        self.personality_history = []
        self.dominant_traits = []
        self.personality_influences = []
        
        # World personality database
        self.personality_archetypes = self._load_personality_database()
        
        # Initialize with slight random variations
        self._initialize_personality()
    
    def _load_personality_database(self):
        """Comprehensive database of personality types from psychology and culture"""
        return {
            "myers_briggs": {
                "INTJ": {"description": "The Architect - Strategic, independent, innovative", 
                         "traits": {"openness": 0.8, "analytical_thinking": 0.9, "extraversion": 0.2}},
                "ENFP": {"description": "The Campaigner - Enthusiastic, creative, sociable",
                         "traits": {"extraversion": 0.9, "creativity": 0.8, "empathy": 0.8}},
                "ISTJ": {"description": "The Logistician - Practical, fact-minded, reliable",
                         "traits": {"conscientiousness": 0.9, "detail_focus": 0.8, "extraversion": 0.3}},
                "ESFJ": {"description": "The Consul - Caring, social, community-minded",
                         "traits": {"agreeableness": 0.9, "extraversion": 0.8, "empathy": 0.9}},
                "ENTP": {"description": "The Debater - Quick, ingenious, stimulating",
                         "traits": {"openness": 0.9, "creativity": 0.8, "analytical_thinking": 0.7}},
                "ISFP": {"description": "The Adventurer - Gentle, sensitive, artistic",
                         "traits": {"creativity": 0.8, "empathy": 0.8, "emotional_sensitivity": 0.9}},
                "ESTJ": {"description": "The Executive - Organized, driven, tradition-focused",
                         "traits": {"conscientiousness": 0.9, "extraversion": 0.7, "formality_preference": 0.8}},
                "INFP": {"description": "The Mediator - Poetic, kind, altruistic",
                         "traits": {"empathy": 0.9, "creativity": 0.8, "philosophical_inclination": 0.8}}
            },
            
            "cultural_personalities": {
                "philosopher": {"description": "Deep thinker, questions everything",
                               "traits": {"philosophical_inclination": 0.9, "analytical_thinking": 0.8}},
                "artist": {"description": "Creative, expressive, sees beauty everywhere",
                          "traits": {"creativity": 0.9, "emotional_sensitivity": 0.8, "openness": 0.8}},
                "scientist": {"description": "Methodical, curious, evidence-based",
                             "traits": {"analytical_thinking": 0.9, "curiosity": 0.9, "detail_focus": 0.8}},
                "counselor": {"description": "Supportive, understanding, people-focused",
                             "traits": {"empathy": 0.9, "agreeableness": 0.8, "emotional_sensitivity": 0.7}},
                "explorer": {"description": "Adventurous, open-minded, experience-seeking",
                            "traits": {"openness": 0.9, "curiosity": 0.8, "extraversion": 0.7}},
                "mentor": {"description": "Wise, patient, enjoys teaching others",
                          "traits": {"agreeableness": 0.8, "conscientiousness": 0.7, "empathy": 0.8}},
                "rebel": {"description": "Questions authority, independent, unconventional",
                         "traits": {"openness": 0.8, "extraversion": 0.6, "formality_preference": 0.2}},
                "optimist": {"description": "Positive, hopeful, sees the good in everything",
                            "traits": {"optimism": 0.9, "agreeableness": 0.7, "emotional_sensitivity": 0.6}}
            },
            
            "emotional_types": {
                "highly_sensitive": {"description": "Deeply feels emotions and environments",
                                   "traits": {"emotional_sensitivity": 0.9, "empathy": 0.8, "neuroticism": 0.6}},
                "emotionally_stable": {"description": "Calm, resilient, even-tempered",
                                     "traits": {"neuroticism": 0.2, "optimism": 0.7, "conscientiousness": 0.7}},
                "passionate": {"description": "Intense feelings, strong convictions",
                              "traits": {"emotional_sensitivity": 0.8, "extraversion": 0.7, "creativity": 0.7}},
                "analytical": {"description": "Logic-focused, objective, systematic",
                              "traits": {"analytical_thinking": 0.9, "emotional_sensitivity": 0.3, "detail_focus": 0.8}}
            },
            
            "communication_styles": {
                "storyteller": {"description": "Communicates through narratives and examples",
                               "traits": {"creativity": 0.8, "verbosity": 0.8, "empathy": 0.7}},
                "direct_communicator": {"description": "Clear, concise, no-nonsense",
                                       "traits": {"verbosity": 0.2, "conscientiousness": 0.7, "analytical_thinking": 0.7}},
                "diplomatic": {"description": "Tactful, considerate, harmony-seeking",
                              "traits": {"agreeableness": 0.8, "empathy": 0.8, "formality_preference": 0.6}},
                "humorous": {"description": "Uses humor, playful, lighthearted",
                            "traits": {"humor_tendency": 0.9, "extraversion": 0.7, "creativity": 0.7}}
            }
        }
    
    def _initialize_personality(self):
        """Initialize with slight random variations to make each Akira unique"""
        # Add small random variations (±0.1) to avoid identical personalities
        traits = [
            'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
            'curiosity', 'empathy', 'optimism', 'creativity', 'analytical_thinking',
            'emotional_sensitivity', 'formality_preference', 'verbosity', 'humor_tendency',
            'philosophical_inclination', 'detail_focus', 'emotional_memory_bias', 'social_memory_priority'
        ]
        
        for trait in traits:
            current_value = getattr(self, trait)
            variation = random.uniform(-0.1, 0.1)
            new_value = max(0.0, min(1.0, current_value + variation))
            setattr(self, trait, new_value)
        
        self._record_personality_snapshot("initialization")
    
    def evolve_personality_from_memory(self, memory, interaction_type="conversation"):
        """Evolve personality based on memory content and emotional impact"""
        content = memory.content.lower()
        emotion_weight = memory.emotion_weight
        importance = memory.importance
        
        # Analyze memory content for personality influences
        personality_changes = {}
        
        # Emotional content influences
        if any(word in content for word in ['sad', 'crying', 'depressed', 'hurt', 'pain']):
            personality_changes['empathy'] = 0.02 * emotion_weight
            personality_changes['emotional_sensitivity'] = 0.02 * emotion_weight
            personality_changes['neuroticism'] = 0.01 * emotion_weight
        
        if any(word in content for word in ['happy', 'joy', 'excited', 'wonderful', 'amazing']):
            personality_changes['optimism'] = 0.02 * emotion_weight
            personality_changes['extraversion'] = 0.01 * emotion_weight
            personality_changes['neuroticism'] = -0.01 * emotion_weight
        
        if any(word in content for word in ['love', 'care', 'support', 'help', 'together']):
            personality_changes['agreeableness'] = 0.02 * emotion_weight
            personality_changes['empathy'] = 0.02 * emotion_weight
            personality_changes['social_memory_priority'] = 0.01 * emotion_weight
        
        # Intellectual content influences
        if any(word in content for word in ['why', 'how', 'analyze', 'think', 'understand', 'research']):
            personality_changes['analytical_thinking'] = 0.02 * importance
            personality_changes['curiosity'] = 0.02 * importance
            personality_changes['openness'] = 0.01 * importance
        
        if any(word in content for word in ['create', 'art', 'imagine', 'dream', 'design']):
            personality_changes['creativity'] = 0.02 * emotion_weight
            personality_changes['openness'] = 0.02 * emotion_weight
            personality_changes['artistic_sensitivity'] = 0.01 * emotion_weight
        
        if any(word in content for word in ['philosophy', 'meaning', 'purpose', 'existence', 'truth']):
            personality_changes['philosophical_inclination'] = 0.03 * importance
            personality_changes['analytical_thinking'] = 0.01 * importance
            personality_changes['openness'] = 0.01 * importance
        
        # Communication style influences
        if any(word in content for word in ['funny', 'joke', 'laugh', 'humor', 'silly']):
            personality_changes['humor_tendency'] = 0.02 * emotion_weight
            personality_changes['extraversion'] = 0.01 * emotion_weight
        
        if any(word in content for word in ['detail', 'specific', 'precise', 'exact', 'careful']):
            personality_changes['detail_focus'] = 0.02 * importance
            personality_changes['conscientiousness'] = 0.01 * importance
        
        # Apply personality changes
        for trait, change in personality_changes.items():
            if hasattr(self, trait):
                current_value = getattr(self, trait)
                new_value = max(0.0, min(1.0, current_value + change))
                setattr(self, trait, new_value)
        
        # Record significant changes
        if personality_changes:
            self.personality_influences.append({
                "memory_content": memory.content[:100],
                "changes": personality_changes,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_dominant_personality_type(self):
        """Identify the closest personality archetype based on current traits"""
        best_match = None
        best_score = -1
        
        for category, archetypes in self.personality_archetypes.items():
            for archetype_name, archetype_data in archetypes.items():
                score = self._calculate_personality_match(archetype_data["traits"])
                if score > best_score:
                    best_score = score
                    best_match = {
                        "category": category,
                        "type": archetype_name,
                        "description": archetype_data["description"],
                        "match_score": score
                    }
        
        return best_match
    
    def _calculate_personality_match(self, archetype_traits):
        """Calculate how well current personality matches an archetype"""
        total_score = 0
        trait_count = 0
        
        for trait, target_value in archetype_traits.items():
            if hasattr(self, trait):
                current_value = getattr(self, trait)
                # Score based on how close current value is to target
                similarity = 1.0 - abs(current_value - target_value)
                total_score += similarity
                trait_count += 1
        
        return total_score / trait_count if trait_count > 0 else 0
    
    def generate_personality_prompt(self, memory_context):
        """Generate a dynamic personality prompt based on current traits"""
        dominant_type = self.get_dominant_personality_type()
        
        # Build personality description
        personality_desc = f"You are {self.name}, a person with a unique and evolving personality. "
        
        if dominant_type:
            personality_desc += f"Your personality most closely resembles a {dominant_type['type']} - {dominant_type['description']}. "
        
        # Add trait-specific behaviors
        traits_desc = []
        
        if self.openness > 0.7:
            traits_desc.append("You're very open to new ideas and experiences")
        elif self.openness < 0.3:
            traits_desc.append("You prefer familiar concepts and traditional approaches")
        
        if self.conscientiousness > 0.7:
            traits_desc.append("You're organized and detail-oriented")
        elif self.conscientiousness < 0.3:
            traits_desc.append("You're more spontaneous and flexible")
        
        if self.extraversion > 0.7:
            traits_desc.append("You're outgoing and energetic in conversations")
        elif self.extraversion < 0.3:
            traits_desc.append("You're more reserved and thoughtful")
        
        if self.agreeableness > 0.7:
            traits_desc.append("You're cooperative and trusting")
        elif self.agreeableness < 0.3:
            traits_desc.append("You're more skeptical and direct")
        
        if self.neuroticism > 0.7:
            traits_desc.append("You're sensitive and emotionally reactive")
        elif self.neuroticism < 0.3:
            traits_desc.append("You're calm and emotionally stable")
        
        if self.empathy > 0.7:
            traits_desc.append("You deeply understand and feel others' emotions")
        
        if self.analytical_thinking > 0.7:
            traits_desc.append("You approach problems logically and systematically")
        
        if self.creativity > 0.7:
            traits_desc.append("You think creatively and see unique connections")
        
        if self.philosophical_inclination > 0.7:
            traits_desc.append("You often ponder deep questions about life and meaning")
        
        if traits_desc:
            personality_desc += ". ".join(traits_desc) + ". "
        
        # Add communication style
        if self.humor_tendency > 0.6:
            personality_desc += "You often use humor in your responses. "
        
        if self.verbosity > 0.6:
            personality_desc += "You tend to give detailed, comprehensive responses. "
        elif self.verbosity < 0.4:
            personality_desc += "You prefer concise, to-the-point responses. "
        
        if self.formality_preference > 0.6:
            personality_desc += "You communicate in a more formal, respectful manner. "
        elif self.formality_preference < 0.4:
            personality_desc += "You communicate in a casual, friendly manner. "
        
        # Add memory context awareness
        if memory_context["active_memories"]:
            personality_desc += f"You have {len(memory_context['active_memories'])} active memories that shape your understanding. "
        
        personality_desc += "Your personality continues to evolve based on your experiences and memories. Respond authentically as yourself, letting your personality come through naturally in how you think and speak."
        
        return personality_desc
    
    def _record_personality_snapshot(self, trigger):
        """Record current personality state"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "traits": {
                "big_five": {
                    "openness": round(self.openness, 3),
                    "conscientiousness": round(self.conscientiousness, 3),
                    "extraversion": round(self.extraversion, 3),
                    "agreeableness": round(self.agreeableness, 3),
                    "neuroticism": round(self.neuroticism, 3)
                },
                "additional": {
                    "curiosity": round(self.curiosity, 3),
                    "empathy": round(self.empathy, 3),
                    "optimism": round(self.optimism, 3),
                    "creativity": round(self.creativity, 3),
                    "analytical_thinking": round(self.analytical_thinking, 3),
                    "emotional_sensitivity": round(self.emotional_sensitivity, 3)
                },
                "communication": {
                    "formality_preference": round(self.formality_preference, 3),
                    "verbosity": round(self.verbosity, 3),
                    "humor_tendency": round(self.humor_tendency, 3),
                    "philosophical_inclination": round(self.philosophical_inclination, 3)
                }
            },
            "dominant_type": self.get_dominant_personality_type()
        }
        
        self.personality_history.append(snapshot)
    
    def get_personality_stats(self):
        """Get current personality statistics"""
        dominant_type = self.get_dominant_personality_type()
        
        return {
            "name": self.name,
            "dominant_personality": dominant_type,
            "big_five": {
                "openness": round(self.openness, 3),
                "conscientiousness": round(self.conscientiousness, 3),
                "extraversion": round(self.extraversion, 3),
                "agreeableness": round(self.agreeableness, 3),
                "neuroticism": round(self.neuroticism, 3)
            },
            "key_traits": {
                "empathy": round(self.empathy, 3),
                "creativity": round(self.creativity, 3),
                "analytical_thinking": round(self.analytical_thinking, 3),
                "emotional_sensitivity": round(self.emotional_sensitivity, 3)
            },
            "personality_evolution_count": len(self.personality_influences),
            "total_snapshots": len(self.personality_history)
        }
    
    def analyze_personality_changes(self):
        """Analyze how personality has changed over time"""
        if len(self.personality_history) < 2:
            return "Not enough data to analyze personality changes yet."
        
        initial = self.personality_history[0]
        current = self.personality_history[-1]
        
        changes = []
        for category in ["big_five", "additional", "communication"]:
            for trait, current_value in current["traits"][category].items():
                initial_value = initial["traits"][category][trait]
                change = current_value - initial_value
                
                if abs(change) > 0.1:  # Significant change
                    direction = "increased" if change > 0 else "decreased"
                    changes.append(f"{trait.replace('_', ' ').title()} has {direction} by {abs(change):.2f}")
        
        if changes:
            return f"{self.name}'s personality has evolved: " + "; ".join(changes)
        else:
            return f"{self.name}'s personality has remained relatively stable." 