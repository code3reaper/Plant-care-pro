import random
from PIL import Image
import os
import logging

# Disease classes that the model can detect
DISEASE_CLASSES = [
    'Healthy',
    'Apple Scab',
    'Apple Black Rot',
    'Apple Cedar Apple Rust',
    'Cherry Powdery Mildew',
    'Cherry Healthy',
    'Corn Gray Leaf Spot',
    'Corn Common Rust',
    'Corn Northern Leaf Blight',
    'Corn Healthy',
    'Grape Black Rot',
    'Grape Esca Black Measles',
    'Grape Leaf Blight',
    'Grape Healthy',
    'Orange Haunglongbing Citrus Greening',
    'Peach Bacterial Spot',
    'Peach Healthy',
    'Pepper Bell Bacterial Spot',
    'Pepper Bell Healthy',
    'Potato Early Blight',
    'Potato Late Blight',
    'Potato Healthy',
    'Raspberry Healthy',
    'Soybean Healthy',
    'Squash Powdery Mildew',
    'Strawberry Leaf Scorch',
    'Strawberry Healthy',
    'Tomato Bacterial Spot',
    'Tomato Early Blight',
    'Tomato Late Blight',
    'Tomato Leaf Mold',
    'Tomato Septoria Leaf Spot',
    'Tomato Spider Mites',
    'Tomato Target Spot',
    'Tomato Yellow Leaf Curl Virus',
    'Tomato Mosaic Virus',
    'Tomato Healthy'
]

# Treatment recommendations for each disease
TREATMENT_RECOMMENDATIONS = {
    'Healthy': {
        'treatment': 'No treatment needed. Continue with regular care and monitoring.',
        'prevention': 'Maintain good agricultural practices: proper spacing, adequate nutrition, and regular monitoring.'
    },
    'Apple Scab': {
        'treatment': 'Apply fungicides like captan or myclobutanil. Remove infected leaves and fruit.',
        'prevention': 'Ensure good air circulation, avoid overhead watering, and plant resistant varieties.'
    },
    'Apple Black Rot': {
        'treatment': 'Remove infected parts, apply copper-based fungicides during dormant season.',
        'prevention': 'Prune for good air circulation, remove mummified fruits, and avoid wounding trees.'
    },
    'Apple Cedar Apple Rust': {
        'treatment': 'Apply preventive fungicides in early spring. Remove nearby cedar trees if possible.',
        'prevention': 'Plant resistant apple varieties and maintain distance from cedar trees.'
    },
    'Cherry Powdery Mildew': {
        'treatment': 'Apply sulfur-based fungicides or neem oil. Improve air circulation.',
        'prevention': 'Avoid overhead watering, ensure proper spacing, and prune for airflow.'
    },
    'Corn Gray Leaf Spot': {
        'treatment': 'Apply fungicides containing azoxystrobin or propiconazole.',
        'prevention': 'Rotate crops, plant resistant varieties, and manage crop residue.'
    },
    'Corn Common Rust': {
        'treatment': 'Apply fungicides if severe. Usually not economically damaging.',
        'prevention': 'Plant resistant hybrids and avoid late planting.'
    },
    'Corn Northern Leaf Blight': {
        'treatment': 'Apply fungicides containing strobilurin or triazole compounds.',
        'prevention': 'Use resistant hybrids, rotate crops, and manage crop residue.'
    },
    'Grape Black Rot': {
        'treatment': 'Apply fungicides like captan or myclobutanil starting at bud break.',
        'prevention': 'Remove mummified berries, prune for air circulation, and avoid overhead irrigation.'
    },
    'Grape Esca Black Measles': {
        'treatment': 'No effective chemical treatment. Remove affected parts and improve vine health.',
        'prevention': 'Avoid pruning wounds, maintain vine vigor, and ensure proper nutrition.'
    },
    'Grape Leaf Blight': {
        'treatment': 'Apply copper-based fungicides or organic fungicides.',
        'prevention': 'Improve air circulation, avoid overhead watering, and remove infected leaves.'
    },
    'Orange Haunglongbing Citrus Greening': {
        'treatment': 'No cure available. Remove infected trees to prevent spread.',
        'prevention': 'Control Asian citrus psyllid vectors and plant certified disease-free trees.'
    },
    'Peach Bacterial Spot': {
        'treatment': 'Apply copper-based bactericides. Avoid overhead irrigation.',
        'prevention': 'Plant resistant varieties, ensure good drainage, and avoid working with wet plants.'
    },
    'Pepper Bell Bacterial Spot': {
        'treatment': 'Apply copper-based bactericides and remove infected plants.',
        'prevention': 'Use disease-free seeds, avoid overhead watering, and rotate crops.'
    },
    'Potato Early Blight': {
        'treatment': 'Apply fungicides containing chlorothalonil or azoxystrobin.',
        'prevention': 'Rotate crops, ensure proper nutrition, and avoid overhead irrigation.'
    },
    'Potato Late Blight': {
        'treatment': 'Apply fungicides containing metalaxyl or dimethomorph immediately.',
        'prevention': 'Use certified seed potatoes, ensure good drainage, and monitor weather conditions.'
    },
    'Squash Powdery Mildew': {
        'treatment': 'Apply sulfur-based fungicides or baking soda solution.',
        'prevention': 'Ensure good air circulation, avoid overhead watering, and plant resistant varieties.'
    },
    'Strawberry Leaf Scorch': {
        'treatment': 'Remove infected leaves and apply fungicides if severe.',
        'prevention': 'Ensure good air circulation, avoid overhead watering, and plant resistant varieties.'
    },
    'Tomato Bacterial Spot': {
        'treatment': 'Apply copper-based bactericides and remove infected plants.',
        'prevention': 'Use disease-free seeds, avoid overhead watering, and practice crop rotation.'
    },
    'Tomato Early Blight': {
        'treatment': 'Apply fungicides containing chlorothalonil or azoxystrobin.',
        'prevention': 'Mulch around plants, avoid overhead watering, and ensure proper spacing.'
    },
    'Tomato Late Blight': {
        'treatment': 'Apply fungicides containing metalaxyl immediately upon detection.',
        'prevention': 'Ensure good air circulation, avoid overhead watering, and monitor humidity.'
    },
    'Tomato Leaf Mold': {
        'treatment': 'Improve ventilation and apply fungicides if in greenhouse.',
        'prevention': 'Reduce humidity, ensure good air circulation, and avoid overhead watering.'
    },
    'Tomato Septoria Leaf Spot': {
        'treatment': 'Apply fungicides containing chlorothalonil or copper compounds.',
        'prevention': 'Mulch soil, avoid overhead watering, and remove infected debris.'
    },
    'Tomato Spider Mites': {
        'treatment': 'Apply miticides or use predatory mites. Increase humidity.',
        'prevention': 'Maintain adequate humidity, avoid drought stress, and encourage beneficial insects.'
    },
    'Tomato Target Spot': {
        'treatment': 'Apply fungicides containing azoxystrobin or chlorothalonil.',
        'prevention': 'Avoid overhead irrigation, ensure good drainage, and rotate crops.'
    },
    'Tomato Yellow Leaf Curl Virus': {
        'treatment': 'No chemical treatment. Remove infected plants and control whiteflies.',
        'prevention': 'Control whitefly vectors, use reflective mulches, and plant resistant varieties.'
    },
    'Tomato Mosaic Virus': {
        'treatment': 'No chemical treatment. Remove infected plants immediately.',
        'prevention': 'Use virus-free seeds, disinfect tools, and avoid handling wet plants.'
    }
}

def create_demo_classifier():
    """Create a demo classifier for demonstration purposes"""
    return {
        'model_type': 'demo_classifier',
        'classes': DISEASE_CLASSES,
        'loaded': True
    }

def load_model():
    """Load the plant disease detection model"""
    try:
        # For demo purposes - in production, load actual TensorFlow model
        model = create_demo_classifier()
        logging.info("Plant disease model loaded successfully (demo mode)")
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def preprocess_image(image):
    """Preprocess the uploaded image for prediction"""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to standard size (224, 224 is common for CNN models)
        image = image.resize((224, 224))
        
        return image
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None

def predict_disease(model, processed_image):
    """Predict plant disease from preprocessed image"""
    try:
        # For demo purposes - in production, use actual model inference
        predicted_disease = random.choice(DISEASE_CLASSES)
        confidence = random.uniform(0.75, 0.95)  # Random confidence between 75-95%
        
        # Get treatment recommendations
        treatment_info = TREATMENT_RECOMMENDATIONS.get(predicted_disease, {
            'treatment': 'Consult with a local agricultural expert for proper diagnosis and treatment.',
            'prevention': 'Follow general good agricultural practices for disease prevention.'
        })
        
        # Generate detailed analysis
        severity_levels = ['Mild', 'Moderate', 'Severe']
        severity = random.choice(severity_levels)
        
        # Extract plant and disease type from disease name
        if ' ' in predicted_disease:
            parts = predicted_disease.split(' ', 1)
            plant_type = parts[0]
            disease_type = parts[1] if len(parts) > 1 else predicted_disease
        else:
            plant_type = 'Unknown'
            disease_type = predicted_disease
        
        # Generate additional details
        affected_areas = ['Leaves', 'Stems', 'Fruits', 'Roots']
        primary_affected = random.choice(affected_areas)
        
        # Time-sensitive recommendations
        immediate_actions = [
            "Remove affected plant parts immediately",
            "Isolate infected plants from healthy ones", 
            "Apply appropriate fungicide/treatment",
            "Improve air circulation around plants",
            "Adjust watering schedule to prevent moisture buildup"
        ]
        
        long_term_actions = [
            "Monitor plants daily for symptom progression",
            "Implement crop rotation in next season",
            "Improve soil drainage and fertility",
            "Use disease-resistant varieties in future plantings",
            "Maintain proper plant spacing for air circulation"
        ]
        
        return {
            'disease': predicted_disease,
            'disease_display_name': disease_type.replace('_', ' ').title(),
            'plant_type': plant_type,
            'confidence': confidence,
            'severity': severity,
            'primary_affected_area': primary_affected,
            'treatment': treatment_info.get('treatment', ''),
            'prevention': treatment_info.get('prevention', ''),
            'immediate_actions': random.sample(immediate_actions, 3),
            'long_term_actions': random.sample(long_term_actions, 3),
            'confidence_level': 'High' if confidence > 0.85 else 'Medium' if confidence > 0.75 else 'Moderate',
            'risk_level': 'High' if severity == 'Severe' else 'Medium' if severity == 'Moderate' else 'Low'
        }
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return {
            'disease': 'Prediction Error',
            'confidence': 0.0,
            'treatment': 'Unable to process image. Please try with a different image.',
            'prevention': 'Ensure image is clear and shows plant leaves clearly.'
        }
