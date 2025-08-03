import numpy as np

def calculate_reward(original_content, new_content):
    # Simple RL reward model based on content similarity and quality
    length_diff = abs(len(original_content) - len(new_content)) / max(len(original_content), len(new_content))
    quality_score = min(len(new_content) / 500, 1.0)  # Proxy for content richness
    reward = (1 - length_diff) * 0.5 + quality_score * 0.5
    return round(reward, 2)