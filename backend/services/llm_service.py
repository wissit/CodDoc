from abc import ABC, abstractmethod
from typing import Dict, Any, List
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic
from config import settings


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def analyze_code(self, code: str, language: str, filename: str = None) -> Dict[str, Any]:
        """Analyze code and return review results."""
        pass
    
    @abstractmethod
    def generate_documentation(self, code: str, language: str, doc_style: str = "google") -> Dict[str, Any]:
        """Generate documentation for code."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_code(self, code: str, language: str, filename: str = None) -> Dict[str, Any]:
        """Analyze code using Gemini."""
        prompt = f"""You are an expert code reviewer. Analyze the following {language} code and provide a comprehensive review.

Code:
```{language}
{code}
```

Provide your analysis in the following JSON format:
{{
    "summary": "Overall assessment of the code quality",
    "quality_score": <number between 0-10>,
    "issues": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "performance|security|maintainability|style|bug",
            "description": "Description of the issue",
            "line_number": <number or null>,
            "suggestion": "How to fix it"
        }}
    ],
    "suggestions": [
        {{
            "title": "Suggestion title",
            "description": "Detailed description",
            "code_example": "Example code or null",
            "priority": "high|medium|low"
        }}
    ],
    "security_concerns": [
        {{
            "severity": "critical|high|medium|low",
            "title": "Security issue title",
            "description": "Description of the security concern",
            "recommendation": "How to address it"
        }}
    ]
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            import json
            # Clean response text
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "summary": f"Error analyzing code: {str(e)}",
                "quality_score": 0,
                "issues": [],
                "suggestions": [],
                "security_concerns": []
            }
    
    def generate_documentation(self, code: str, language: str, doc_style: str = "google") -> Dict[str, Any]:
        """Generate documentation using Gemini."""
        prompt = f"""You are an expert technical writer. Generate comprehensive documentation for the following {language} code in {doc_style} style.

Code:
```{language}
{code}
```

Provide documentation in the following JSON format:
{{
    "overview": "High-level description of what this code does",
    "functions": [
        {{
            "name": "function_name",
            "description": "What the function does",
            "parameters": [
                {{
                    "name": "param_name",
                    "type": "param_type",
                    "description": "Parameter description"
                }}
            ],
            "returns": {{
                "type": "return_type",
                "description": "What is returned"
            }},
            "examples": ["Example usage code"]
        }}
    ],
    "classes": [
        {{
            "name": "ClassName",
            "description": "What the class does",
            "attributes": [
                {{
                    "name": "attr_name",
                    "type": "attr_type",
                    "description": "Attribute description"
                }}
            ],
            "methods": [<same structure as functions>]
        }}
    ],
    "usage_examples": ["Complete usage examples"]
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            import json
            # Clean response text
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "overview": f"Error generating documentation: {str(e)}",
                "functions": [],
                "classes": [],
                "usage_examples": []
            }


class OpenAIProvider(LLMProvider):
    """OpenAI GPT LLM provider."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def analyze_code(self, code: str, language: str, filename: str = None) -> Dict[str, Any]:
        """Analyze code using OpenAI."""
        prompt = f"""You are an expert code reviewer. Analyze the following {language} code and provide a comprehensive review.

Code:
```{language}
{code}
```

Provide your analysis in valid JSON format with: summary, quality_score (0-10), issues array, suggestions array, and security_concerns array."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            import json
            text = response.choices[0].message.content.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "summary": f"Error analyzing code: {str(e)}",
                "quality_score": 0,
                "issues": [],
                "suggestions": [],
                "security_concerns": []
            }
    
    def generate_documentation(self, code: str, language: str, doc_style: str = "google") -> Dict[str, Any]:
        """Generate documentation using OpenAI."""
        prompt = f"""Generate comprehensive documentation for the following {language} code in {doc_style} style.

Code:
```{language}
{code}
```

Provide documentation in valid JSON format with: overview, functions array, classes array, and usage_examples array."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            import json
            text = response.choices[0].message.content.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "overview": f"Error generating documentation: {str(e)}",
                "functions": [],
                "classes": [],
                "usage_examples": []
            }


class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM provider."""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def analyze_code(self, code: str, language: str, filename: str = None) -> Dict[str, Any]:
        """Analyze code using Claude."""
        prompt = f"""Analyze the following {language} code and provide a comprehensive review in valid JSON format.

Code:
```{language}
{code}
```

Return JSON with: summary, quality_score (0-10), issues, suggestions, and security_concerns."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            import json
            text = response.content[0].text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "summary": f"Error analyzing code: {str(e)}",
                "quality_score": 0,
                "issues": [],
                "suggestions": [],
                "security_concerns": []
            }
    
    def generate_documentation(self, code: str, language: str, doc_style: str = "google") -> Dict[str, Any]:
        """Generate documentation using Claude."""
        prompt = f"""Generate comprehensive documentation for the following {language} code in {doc_style} style. Return valid JSON only.

Code:
```{language}
{code}
```

Return JSON with: overview, functions, classes, and usage_examples."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            import json
            text = response.content[0].text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "overview": f"Error generating documentation: {str(e)}",
                "functions": [],
                "classes": [],
                "usage_examples": []
            }


class LLMService:
    """Service for managing multiple LLM providers."""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available LLM providers based on API keys."""
        if settings.gemini_api_key:
            self.providers["gemini"] = GeminiProvider(settings.gemini_api_key)
        
        if settings.openai_api_key:
            self.providers["openai"] = OpenAIProvider(settings.openai_api_key)
        
        if settings.anthropic_api_key:
            self.providers["anthropic"] = AnthropicProvider(settings.anthropic_api_key)
    
    def get_provider(self, provider_name: str = None) -> LLMProvider:
        """Get LLM provider by name or default."""
        if provider_name is None:
            provider_name = settings.default_llm_provider
        
        if provider_name not in self.providers:
            raise ValueError(f"LLM provider '{provider_name}' not available. Available providers: {list(self.providers.keys())}")
        
        return self.providers[provider_name]
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available providers."""
        provider_info = {
            "gemini": {"name": "Google Gemini", "models": ["gemini-pro"]},
            "openai": {"name": "OpenAI GPT", "models": ["gpt-4", "gpt-3.5-turbo"]},
            "anthropic": {"name": "Anthropic Claude", "models": ["claude-3-sonnet", "claude-3-opus"]}
        }
        
        return [
            {
                "id": key,
                "name": provider_info[key]["name"],
                "models": provider_info[key]["models"],
                "default": key == settings.default_llm_provider
            }
            for key in self.providers.keys()
        ]


# Global LLM service instance
llm_service = LLMService()
