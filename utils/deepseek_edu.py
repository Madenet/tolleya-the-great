import json
import requests
from django.conf import settings
from django.utils import timezone
from questpaper.models import *
from main_app.models import *

def get_deepseek_response(prompt, model="deepseek-chat", max_tokens=2048):
    """
    Get response from DeepSeek Chat API
    """
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(settings.DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API Error: {e}")
        return "I'm currently unable to process your request. Please try again later."

def get_education_context(question_type, question, request=None):
    """Generate context-aware prompts for educational queries"""
    
    base_context = f"""
    You are DeepSeek-Edu, the AI assistant for thecms.co.za's Circuit Management System.
    Current user: {request.user.username if request.user.is_authenticated else 'Guest'}
    """
    
    if question_type == 'career':
        return f"""
        {base_context}
        Provide detailed career guidance including:
        - Required subjects/skills
        - Potential institutions
        - Career growth prospects
        - Industry demand
        - Salary expectations in South Africa
        - Professional bodies
        
        Question: {question}
        """
    
    elif question_type == 'prospector':
        colleges = CollegeAndUniversities.objects.using('cms_db').values_list('name', flat=True)
        return f"""
        {base_context}
        As an undergraduate prospector advisor, provide information on:
        - Admission requirements
        - Application deadlines
        - Available programs at: {', '.join(colleges)[:500]}
        - NSFAS and funding options
        - Campus life preparation
        
        Question: {question}
        """
    
    elif question_type == 'bursary':
        active_bursaries = Bursary.objects.using('cms_db').filter(deadline__gte=timezone.now())
        return f"""
        {base_context}
        Current active bursaries: {', '.join(b.name for b in active_bursaries)[:300]}
        
        Provide information about:
        - Bursary eligibility
        - Application processes
        - Required documents
        - Alternative funding options
        - Repayment obligations
        
        Question: {question}
        """
    
    elif question_type in ['assessment', 'memorandum']:
        return f"""
        {base_context}
        As an educational content specialist, you may:
        - Explain concepts (without providing direct answers)
        - Solve example problems
        - Provide study techniques
        - Clarify marking rubrics
        - Suggest learning resources
        
        Question: {question}
        
        Important: For memorandums, only provide verified answers or guide to solutions.
        """
    
    else:  # school management
        return f"""
        {base_context}
        As a CMS expert, provide guidance on:
        - School administration
        - Curriculum management
        - Teacher support
        - Student records
        - Reporting features in ElimCircuit
        
        Question: {question}
        """