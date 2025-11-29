"""
Medical Imaging Analysis Tools
Provides AI-powered analysis of medical images using Gemini Vision
"""
import os
import base64
from typing import Dict, Any, Optional
from pathlib import Path
import google.generativeai as genai
from crewai.tools import tool
from .utils.logging import get_logger
from .config import GOOGLE_API_KEY, GEMINI_MODEL

logger = get_logger(__name__)


def _configure_genai():
    """Configure Google Generative AI with API key"""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not configured")
    genai.configure(api_key=GOOGLE_API_KEY)


def _encode_image(image_path: str) -> str:
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@tool("medical_image_analysis")
def medical_image_analysis(image_path: str, patient_context: str = "") -> Dict[str, Any]:
    """
    Analyze medical images (X-ray, MRI, CT scan) using Gemini Vision AI.
    
    Args:
        image_path: Path to the medical image file
        patient_context: Optional patient context (symptoms, demographics, history)
    
    Returns:
        Dictionary with analysis results including:
        - image_type: Modality and anatomical region
        - findings: Key observations and abnormalities
        - assessment: Diagnostic assessment with confidence
        - patient_explanation: Simple language explanation
        - severity: Normal/Mild/Moderate/Severe
    """
    try:
        _configure_genai()
        
        # Validate image path
        if not Path(image_path).exists():
            return {
                "error": f"Image file not found: {image_path}",
                "status": "failed"
            }
        
        # Create the model
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Prepare the analysis prompt
        context_section = f"### Patient Context\n{patient_context}\n\n" if patient_context else ""
        
        prompt = f"""You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging.

Analyze this medical image and provide a structured response:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify anatomical region and positioning
- Comment on image quality and technical adequacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level (Low/Medium/High)
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain findings in simple, clear language
- Avoid medical jargon or provide clear definitions
- Address common patient concerns

{context_section}Format your response as valid JSON with these keys:
- image_type: {{modality, region, quality}}
- findings: [list of observations with severity]
- assessment: {{primary_diagnosis, confidence, differentials, critical_flags}}
- patient_explanation: string
- severity: "Normal"/"Mild"/"Moderate"/"Severe"
"""
        
        # Load and analyze image
        logger.info(f"Analyzing medical image: {image_path}")
        
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # Generate content with image
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        result = {
            "status": "success",
            "analysis": response.text,
            "image_path": image_path,
            "model_used": GEMINI_MODEL
        }
        
        logger.info("Medical image analysis completed successfully")
        return result
        
    except Exception as e:
        logger.exception(f"Medical image analysis failed: {e}")
        return {
            "error": str(e),
            "status": "failed",
            "image_path": image_path
        }


@tool("extract_imaging_findings")
def extract_imaging_findings(analysis_result: Dict[str, Any]) -> str:
    """
    Extract and summarize key findings from imaging analysis result.
    
    Args:
        analysis_result: Result dictionary from medical_image_analysis
    
    Returns:
        Formatted summary of imaging findings
    """
    try:
        if analysis_result.get("status") == "failed":
            return f"Imaging analysis failed: {analysis_result.get('error', 'Unknown error')}"
        
        analysis_text = analysis_result.get("analysis", "")
        
        summary = f"""
### Medical Imaging Summary

**Status**: {analysis_result.get('status', 'unknown')}
**Model**: {analysis_result.get('model_used', 'N/A')}

{analysis_text}

---
*This analysis was generated by AI and should be reviewed by a qualified radiologist.*
"""
        return summary.strip()
        
    except Exception as e:
        logger.exception(f"Failed to extract imaging findings: {e}")
        return f"Error extracting findings: {e}"


@tool("compare_imaging_timeline")
def compare_imaging_timeline(
    current_image_path: str,
    previous_image_path: Optional[str] = None,
    patient_context: str = ""
) -> Dict[str, Any]:
    """
    Compare current medical image with previous imaging to track disease progression.
    
    Args:
        current_image_path: Path to current medical image
        previous_image_path: Optional path to previous image for comparison
        patient_context: Patient context and history
    
    Returns:
        Comparison analysis with progression notes
    """
    try:
        _configure_genai()
        
        if not previous_image_path:
            # Just analyze current image
            return medical_image_analysis(current_image_path, patient_context)
        
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        context_section = f"### Patient Context\n{patient_context}\n\n" if patient_context else ""
        
        prompt = f"""You are a medical imaging expert comparing sequential medical images.

Analyze these images chronologically and provide:

### 1. Temporal Comparison
- Describe changes between images
- Note progression, improvement, or stability
- Highlight new findings or resolved conditions

### 2. Clinical Significance
- Assess disease progression or treatment response
- Rate change: Improved/Stable/Worsened
- Recommend follow-up imaging timeline

### 3. Summary
- Concise clinical summary of imaging timeline
- Recommendations for ongoing monitoring

{context_section}"""
        
        logger.info(f"Comparing images: {previous_image_path} → {current_image_path}")
        
        # Load both images
        with open(previous_image_path, 'rb') as prev_file, open(current_image_path, 'rb') as curr_file:
            prev_data = prev_file.read()
            curr_data = curr_file.read()
        
        response = model.generate_content([
            prompt,
            "Previous Image:",
            {"mime_type": "image/jpeg", "data": prev_data},
            "Current Image:",
            {"mime_type": "image/jpeg", "data": curr_data}
        ])
        
        return {
            "status": "success",
            "comparison": response.text,
            "previous_image": previous_image_path,
            "current_image": current_image_path,
            "model_used": GEMINI_MODEL
        }
        
    except Exception as e:
        logger.exception(f"Image comparison failed: {e}")
        return {
            "error": str(e),
            "status": "failed"
        }
