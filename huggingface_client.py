import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models"

def generate_with_hf(prompt, model="gpt2", max_tokens=300, temperature=0.7):
    """
    Generate text using HF inference API
    Returns: (success: bool, text: str)
    """
    if not HF_TOKEN:
        return False, "No HF_TOKEN found"
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    url = f"{HF_API_URL}/{model}"
    
    # Convert tokens properly for consistency
    min_tokens = int(max_tokens * 0.7)
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "min_new_tokens": min_tokens,
            "temperature": temperature,
            "do_sample": True,
            "top_p": 0.95,
            "details": True
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Log the status
        print(f"[{model}] Status: {response.status_code}")
        
        # Handle different status codes
        if response.status_code == 200:
            data = response.json()
            # API returns list of dicts with 'generated_text'
            if isinstance(data, list) and len(data) > 0:
                text = data[0].get("generated_text", "")
                if len(text.strip()) > 10:
                    return True, text
            return False, "Empty response"
        
        elif response.status_code == 429:
            return False, "Rate limited (429)"
        elif response.status_code == 503:
            return False, "Service unavailable (503)"
        elif response.status_code == 410:
            return False, "Model deprecated (410)"
        elif response.status_code == 403:
            return False, "Forbidden - check token (403)"
        else:
            return False, f"Error {response.status_code}"
    
    except requests.Timeout:
        return False, "Request timeout"
    except Exception as e:
        return False, str(e)


def generate_with_local(prompt, max_tokens=300, temperature=0.7, target_words=300):
    """
    Local rule-based story generation - expanded based on word count
    Returns: (success: bool, text: str)
    """
    try:
        import random
        
        # Clean the prompt
        if "approximately" in prompt:
            prompt = prompt.split("about")[-1].split("that")[0].strip()
        
        prompt = prompt.lower().strip()
        
        # Use actual target_words instead of calculating from tokens
        # This is passed from generate_story
        
        # Story building blocks - increase based on target word count
        if target_words < 150:
            # Very short: 5 sentences (~100-130 words, ~20-25 words each)
            sentences = [
                f"In a mystical realm, {prompt} emerged from ancient mists, bringing both wonder and danger to all who beheld it.",
                f"The heroes gathered with courage burning in their hearts, knowing {prompt} was their only hope for salvation against the darkness.",
                f"A great battle erupted when {prompt} revealed its true nature, testing the resolve of even the bravest warriors.",
                f"With determination in their eyes, they prepared for the final confrontation, ready to face victory or death.",
                f"Against impossible odds, they triumphed gloriously, and {prompt} became the greatest legend of the age, remembered forever.",
            ]
        elif target_words < 250:
            # Short: 8 sentences (~150-230 words, ~25-30 words each)
            sentences = [
                f"In a mystical realm far from the lands of men, {prompt} emerged from ancient mists that shrouded the mountains, bringing both wonder and terrible danger.",
                f"The ancient prophecy had spoken of {prompt} and the great deeds it would accomplish in the world, changing the fate of nations.",
                f"The heroes gathered from across the kingdom with courage burning bright in their hearts, knowing {prompt} was their only hope for salvation.",
                f"Together they journeyed across dangerous lands and through treacherous forests, discovering truths about {prompt} that had been hidden for generations.",
                f"The magic surrounding {prompt} was far stronger than anyone had anticipated, testing their resolve and courage at every single turn.",
                f"Great battles erupted across the landscape as {prompt} revealed powers beyond the imagination of mortals, shaking the very foundations of the earth.",
                f"With unwavering determination shining in their eyes, they prepared for the ultimate confrontation, knowing only victory or death awaited them.",
                f"Against impossible odds and overwhelming enemies, they triumphed magnificently. {prompt} became the greatest legend ever known, remembered in songs forever.",
            ]
        elif target_words < 400:
            # Medium: 11 sentences (~250-380 words, ~30-35 words each)
            sentences = [
                f"In a mystical realm far from the lands of men, where magic flowed like rivers, {prompt} emerged from ancient mists that had shrouded the mountains for countless centuries.",
                f"The ancient prophecy had been carved in stone by the greatest seers of old, and it spoke with certainty of {prompt} and the magnificent deeds it would accomplish.",
                f"For generations beyond count, people had waited and hoped for this momentous occasion. When it finally came, the heroes gathered with unshakeable courage burning bright.",
                f"They knew with absolute certainty that {prompt} was their only hope for salvation, their last chance to save their beloved kingdom from the encroaching darkness.",
                f"Together, bound by destiny and friendship, they undertook an epic journey across dangerous lands and through dense treacherous forests filled with ancient magic and peril.",
                f"Along the way, they discovered profound secrets about {prompt} that had been carefully hidden and protected for countless ages by those who came before them.",
                f"The magic surrounding {prompt} was far stronger and infinitely more complex than anyone, even the wisest sages, had ever anticipated in their wildest dreams.",
                f"Great battles erupted across the landscape like wildfire, with ancient magic clashing violently against forged steel as {prompt} revealed powers beyond mortal comprehension.",
                f"Sacrifices were made along the treacherous way, and some of the bravest warriors fell in glorious battle defending their companions and their noble cause.",
                f"With unwavering determination shining brilliantly in their eyes, they prepared for the ultimate final confrontation involving {prompt}, knowing only victory or death awaited.",
                f"Against impossible odds that would have broken lesser warriors, they triumphed magnificently and gloriously. {prompt} became the greatest legend the world had ever known.",
            ]
        elif target_words < 600:
            # Long: 14 sentences (~400-580 words, ~35-42 words each)
            sentences = [
                f"In a mystical realm far from the lands of men, where magic flowed like rivers through enchanted valleys, {prompt} emerged from ancient mists that had shrouded the towering mountains for countless centuries.",
                f"The ancient prophecy had been carved in stone by the greatest seers of old, written in languages long forgotten, and it spoke with absolute certainty of {prompt} and the magnificent deeds it would accomplish.",
                f"For generations beyond count, spanning hundreds of years through times of war and peace, people had waited and hoped for this momentous occasion that would change everything they knew.",
                f"When it finally came upon them like a storm, the bravest heroes from across the kingdom gathered together with unshakeable courage burning bright in their hearts, ready to face any challenge.",
                f"They knew with absolute certainty, without any doubt in their minds, that {prompt} was their only hope for salvation and survival, their last chance to save their beloved kingdom.",
                f"Together, bound by destiny and unbreakable friendship, they undertook an epic journey across dangerous and unforgiving lands, through dense treacherous forests filled with ancient magic, over towering mountains that pierced the heavens.",
                f"Along their perilous journey, they discovered profound and earth-shattering secrets about {prompt} that had been carefully hidden and zealously protected for countless ages by the ancient guardians who came before.",
                f"The magic surrounding {prompt} was far stronger, more powerful, and infinitely more complex than anyone, even the wisest sages and most learned scholars, had ever anticipated in their wildest dreams.",
                f"Great and terrible battles erupted across the landscape like wildfire spreading through dry grass, with ancient magic clashing violently against forged steel and burning fire in spectacular displays of raw power.",
                f"Sacrifices were made along the treacherous way, and some of the bravest and most noble warriors fell in glorious battle, but their legacy lived on eternally in the hearts of those who continued fighting.",
                f"The enemy grew desperate and more dangerous as the heroes approached their final destination, launching wave after wave of increasingly ferocious attacks in a desperate attempt to stop them.",
                f"With unwavering determination shining brilliantly like stars in their eyes, never faltering for even a moment, they prepared themselves mentally and physically for the ultimate final confrontation involving {prompt}.",
                f"Against impossible odds that would have broken lesser warriors, facing enemies that outnumbered them a hundred to one, they fought with everything they had and triumphed magnificently through sheer courage.",
                f"When the dust finally settled and the last enemy had fallen defeated, {prompt} became the greatest legend the world had ever known, a story that would echo through history forever.",
            ]
        else:
            # Epic: 17 long sentences (~600-850 words, ~45-50 words each)
            sentences = [
                f"In a mystical realm far from the lands of men, where magic flowed like rivers through enchanted valleys and mountains touched the clouds, {prompt} emerged from ancient mists that had shrouded the land for countless centuries, bringing both wonder and terrible danger to all who beheld it.",
                f"The ancient prophecy had been carved in stone by the greatest seers of old, written in languages long forgotten by mortal minds, and it spoke with certainty of {prompt} and the magnificent deeds it would accomplish in the world, changing the very fabric of reality itself.",
                f"For generations beyond count, spanning hundreds of years through times of war and peace, people had waited and hoped for this momentous occasion. When it finally came upon them like a storm, the bravest heroes from across the kingdom gathered together with unshakeable courage burning bright in their hearts.",
                f"They knew with absolute certainty, without any doubt in their minds, that {prompt} was their only hope for salvation and survival, their last and final chance to save their beloved kingdom and all they held dear from the encroaching darkness that threatened to consume everything.",
                f"Together, bound by destiny and friendship that had been forged through countless trials, they undertook an epic journey across dangerous and unforgiving lands, through dense treacherous forests filled with ancient magic and creatures of nightmare, over towering mountains that pierced the heavens themselves.",
                f"Along their perilous journey through lands both beautiful and terrible, they discovered profound secrets about {prompt} that had been carefully hidden and zealously protected for countless ages by the ancient guardians and wise keepers who came before them in ages past.",
                f"The magic surrounding {prompt} was far stronger, more powerful, and infinitely more complex than anyone, even the wisest sages, most learned scholars, and ancient mystics had ever anticipated in their wildest dreams. It tested their resolve, their courage, and their very souls at every single turn.",
                f"Great and terrible battles erupted across the landscape like wildfire spreading through dry grass, with ancient magic clashing violently against forged steel and burning fire, as {prompt} revealed powers and abilities that went far beyond the imagination and comprehension of mere mortals, shaking the foundations of the world itself.",
                f"Sacrifices were made along the treacherous way, hearts were broken, and some of the bravest and most noble warriors fell in glorious battle fighting to their last breath, but their noble legacy and memory lived on eternally in the hearts and minds of those who continued to fight the good fight.",
                f"The enemy grew desperate and more dangerous as the heroes approached their final destination, launching wave after wave of attacks with increasing ferocity and madness, throwing everything they had in a desperate attempt to stop the heroes from reaching their goal and fulfilling the ancient prophecy.",
                f"Dark magic filled the skies, the earth trembled beneath their feet, and the very fabric of reality seemed to tear as the forces of darkness made their final desperate stand against the heroes who carried the hope of the world on their shoulders.",
                f"Epic battles of legendary proportion erupted across the entire landscape, with magic clashing against steel in spectacular displays of power that lit up the sky like a thousand suns, creating explosions of light and shadow that could be seen from kingdoms away.",
                f"With unwavering determination shining brilliantly like stars in their eyes, never faltering for even a moment despite exhaustion and pain, they prepared themselves mentally and physically for the ultimate final confrontation involving {prompt}, knowing full well that only complete victory or glorious death awaited them at the end of this journey.",
                f"Against impossible odds that would have broken lesser warriors and driven strong men mad with fear, facing enemies that outnumbered them a hundred to one, they fought with everything they had. Through skill, courage, determination, and the power of {prompt}, they triumphed magnificently and gloriously over the forces of darkness.",
                f"When the dust finally settled over the battlefield and the last enemy had fallen defeated and broken, {prompt} became the greatest legend the world had ever known, a story that would echo through the halls of history for all time, inspiring countless generations yet to come.",
                f"Kingdoms that had warred for centuries were finally united under the banner of peace and mutual respect, prosperity and abundance was restored to lands that had known only suffering and despair, and the entire world entered a new golden age of enlightenment, harmony, and hope for the future.",
                f"The epic tale of {prompt} would be told and retold for countless generations to come, remembered forever in songs sung by bards in great halls, in stories cherished and passed down by grandparents to wide-eyed children gathered around warm fires, and in the hearts of all people who believed in the power of courage and hope.",
            ]
        
        # Build story by joining sentences
        text = " ".join(sentences)
        
        if text and len(text.strip()) > 30:
            return True, text
        return False, "Failed to generate story"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def generate_story(prompt, genre="Fantasy", creativity=0.7, max_length=300):
    """
    Main story generation function - always returns instantly
    1. Try HF API (will fail on free tier)
    2. Use rule-based fallback (instant)
    """
    models = ["gpt2"]  # Only try gpt2 for speed
    
    # Convert words to tokens
    max_tokens = int(max_length * 1.33)
    max_tokens = min(max_tokens, 800)
    
    # Create the HF prompt for API (if it works)
    hf_prompt = f"Write a creative {genre} story about {prompt} that is approximately {max_length} words long.\n\n"
    
    # Quick HF API attempt (will timeout or return 410)
    success, text = generate_with_hf(hf_prompt, "gpt2", max_tokens, creativity)
    if success:
        return trim_to_word_count(text, max_length)
    
    # Fallback to instant rule-based generation - pass clean prompt and target word count
    success, text = generate_with_local(prompt, max_tokens, creativity, target_words=max_length)
    if success:
        return trim_to_word_count(text, max_length)
    
    # Final fallback - always works
    return build_story_to_length(prompt, max_length, genre)


def trim_to_word_count(text, target_words):
    """Trim or pad text to target word count"""
    words = text.split()
    
    if len(words) <= target_words:
        return text  # Keep as is if under target
    
    # Trim to target length
    trimmed = " ".join(words[:target_words])
    # Add ellipsis only if we actually trimmed
    if len(words) > target_words:
        trimmed += "..."
    return trimmed


def build_story_to_length(prompt, target_words, genre):
    """Build a story to exact word length"""
    import random
    
    # Sentence fragments of varying lengths
    short_fragments = [
        f"In the beginning, {prompt.lower()} awakened with tremendous power.",
        f"{prompt.capitalize()} was legendary beyond all measure.",
        f"The hero found {prompt.lower()} in the depths of an ancient temple.",
        f"Magic surrounded {prompt.lower()} like an invisible cloak.",
    ]
    
    medium_fragments = [
        f"In a mystical realm, {prompt.lower()} emerged from ancient mists, bringing both wonder and danger to all who beheld it. Legends spoke of its power across the known world.",
        f"{prompt.capitalize()} had the power to change worlds forever. The prophecy had spoken of this moment for a thousand years, whispered by seers and encoded in ancient texts.",
        f"When {prompt.lower()} finally awakened, the ground trembled and the sky split with thunder. The very fabric of reality seemed to tear asunder.",
        f"The heroes set out to find {prompt.lower()}. They knew that only it could save their kingdom from the approaching darkness and destruction.",
        f"A great journey began when {prompt.lower()} appeared. It would test the courage of all who dared to follow its path through danger and uncertainty.",
    ]
    
    long_fragments = [
        f"In a world where magic flowed like rivers through enchanted lands, {prompt.lower()} was spoken of in whispered tales by scholars and warriors alike. Its power was said to be immense beyond measure. Kings and queens sought it, armies marched for it, and heroes died in pursuit of it.",
        f"{prompt.capitalize()} had slumbered for countless ages in the depths of ancient mountains and forgotten temples, waiting for the day when it would be needed most by mortals. When it finally stirred, the world would never be the same again.",
        f"The prophecy was ancient, carved in stone by seers who looked into the threads of fate itself. It told of {prompt.lower()} and the great deeds it would accomplish. Every word had been preserved through the ages, passed down carefully from generation to generation.",
        f"A band of brave heroes set forth on a perilous quest across dangerous lands, through dark forests and treacherous mountains, all seeking {prompt.lower()}. They faced countless obstacles and dangers, yet none could turn them back from their noble purpose.",
        f"When the final battle came, {prompt.lower()} stood at the center of the conflict, its power radiating outward like waves from a stone cast into still water. The very ground shook with the force of its magic.",
    ]
    
    epic_fragments = [
        f"In a time when the world was young and magic flowed freely through every living thing, there existed a power of extraordinary significance known as {prompt.lower()}. This magnificent force had shaped the course of civilizations and would continue to do so for all ages to come. Warriors and scholars devoted their entire lives to understanding its mysteries and learning to harness its incredible potential.",
        f"{prompt.capitalize()} was far more than a mere object or concept. It represented the pinnacle of magical achievement, the embodiment of ancient wisdom passed down through countless generations. Those who sought it understood that finding {prompt.lower()} would change their lives forever and perhaps save their entire world from impending darkness.",
        f"The heroes undertook a quest of legendary proportions, facing unimaginable dangers and trials beyond their wildest dreams. They crossed treacherous lands, battled fierce creatures, and overcame seemingly insurmountable obstacles. All of this was done in pursuit of {prompt.lower()}. And when at last they succeeded, they discovered that the true power lay not in {prompt.lower()} itself, but in the strength of their unity and determination.",
    ]
    
    # Build story based on target length
    if target_words <= 50:
        # Very short story
        return " ".join([
            random.choice(short_fragments),
            random.choice(short_fragments),
            "Victory was theirs."
        ])
    
    elif target_words <= 100:
        # Short story
        text = " ".join([
            random.choice(short_fragments),
            random.choice(medium_fragments),
            f"The legend of {prompt.lower()} lived on."
        ])
    
    elif target_words <= 200:
        # Medium story
        text = " ".join([
            random.choice(medium_fragments),
            random.choice(medium_fragments),
            random.choice(long_fragments),
        ])
    
    elif target_words <= 500:
        # Long story
        text = " ".join([
            random.choice(medium_fragments),
            random.choice(long_fragments),
            random.choice(long_fragments),
            f"And so {prompt.lower()} became eternal.",
        ])
    
    else:
        # Epic story
        text = " ".join([
            random.choice(long_fragments),
            random.choice(epic_fragments),
            random.choice(long_fragments),
            f"The age of {prompt.lower()} had begun, and it would be remembered forever in the annals of history."
        ])
    
    # Trim to exact word count
    words = text.split()
    if len(words) > target_words:
        text = " ".join(words[:target_words]) + "..."
    
    return text
