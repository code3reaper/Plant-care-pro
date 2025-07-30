import json
import logging
import os
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_HARDCODED_GEMINI_API_KEY"))

def get_ai_response(user_message):
    """Get AI response for agricultural questions using Gemini"""
    try:
        # System prompt for agricultural assistant
        system_prompt = """You are an expert agricultural assistant specializing in:
        - Plant disease identification and treatment
        - Crop care and farming best practices
        - Pest management and prevention
        - Soil health and nutrition
        - Weather-related farming advice
        - Sustainable farming techniques
        
        Provide helpful, accurate, and practical advice for farmers and gardeners.
        Format your responses with clear structure:
        - Use numbered lists for step-by-step instructions
        - Use bullet points for key points
        - Bold important terms with **bold text**
        - Provide complete, detailed responses
        Always prioritize plant and human safety and give comprehensive answers."""
        
        # Create the content with system instruction
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_message)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
                max_output_tokens=2000
            )
        )
        
        if response.text:
            # Format the response for better display
            formatted_response = format_ai_response(response.text)
            return formatted_response
        else:
            return "I'm sorry, I couldn't generate a response. Please try again."
            
    except Exception as e:
        logging.error(f"Error getting AI response: {e}")
        return "I'm experiencing technical difficulties. Please try again later."

def format_ai_response(text):
    """Format AI response text for better HTML display"""
    import re
    
    if not text or not text.strip():
        return "No response generated."
    
    # Clean up the text first
    formatted = text.strip()
    
    # Format bold text (markdown style) - do this first
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-primary">\1</strong>', formatted)
    
    # Format italic text
    formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
    
    # Split into paragraphs and handle each
    paragraphs = formatted.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
            
        # Handle numbered lists
        if re.search(r'^\d+\.', paragraph.strip()):
            lines = paragraph.split('\n')
            list_items = []
            for line in lines:
                if line.strip():
                    # Check if it's a numbered item
                    if re.match(r'^\d+\.', line.strip()):
                        list_items.append(f'<div class="mb-2"><strong class="text-success">{line.strip()}</strong></div>')
                    else:
                        # It's a continuation of the previous item
                        if list_items:
                            list_items[-1] = list_items[-1].replace('</div>', f' {line.strip()}</div>')
                        else:
                            list_items.append(f'<div class="mb-2">{line.strip()}</div>')
            formatted_paragraphs.append('<div class="mb-3">' + ''.join(list_items) + '</div>')
        
        # Handle bullet points
        elif re.search(r'^[*•-]', paragraph.strip()):
            lines = paragraph.split('\n')
            list_items = []
            for line in lines:
                if line.strip():
                    if re.match(r'^[*•-]', line.strip()):
                        clean_line = re.sub(r'^[*•-]\s*', '', line.strip())
                        list_items.append(f'<div class="mb-2"><span class="text-success me-2">•</span>{clean_line}</div>')
                    else:
                        if list_items:
                            list_items[-1] = list_items[-1].replace('</div>', f' {line.strip()}</div>')
                        else:
                            list_items.append(f'<div class="mb-2">{line.strip()}</div>')
            formatted_paragraphs.append('<div class="mb-3">' + ''.join(list_items) + '</div>')
        
        # Regular paragraphs
        else:
            # Handle line breaks within paragraphs
            lines = paragraph.split('\n')
            paragraph_content = '<br>'.join([line.strip() for line in lines if line.strip()])
            if paragraph_content:
                formatted_paragraphs.append(f'<div class="mb-3">{paragraph_content}</div>')
    
    # Join all formatted paragraphs
    result = ''.join(formatted_paragraphs)
    
    # If no formatting was applied, wrap in a simple div
    if not result:
        result = f'<div class="mb-3">{formatted}</div>'
    
    return result

def analyze_plant_image_with_ai(image_path):
    """Analyze plant image using Gemini Vision"""
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                "Analyze this plant image for signs of disease, pests, or health issues. Provide detailed observations about leaf color, texture, spots, or other abnormalities. Also suggest possible causes and treatments if any issues are detected."
            ],
        )
        
        return response.text if response.text else "Unable to analyze the image."
        
    except Exception as e:
        logging.error(f"Error analyzing image with AI: {e}")
        return "Error analyzing image. Please try again."
