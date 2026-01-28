import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Types
export interface AnalyzeRequest {
    code: string;
    language: string;
    filename?: string;
    llm_provider?: string;
}

export interface CodeIssue {
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    category: string;
    description: string;
    line_number?: number;
    suggestion: string;
}

export interface Suggestion {
    title: string;
    description: string;
    code_example?: string;
    priority: 'high' | 'medium' | 'low';
}

export interface SecurityConcern {
    severity: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    recommendation: string;
}

export interface Analysis {
    summary: string;
    quality_score: number;
    issues: CodeIssue[];
    suggestions: Suggestion[];
    security_concerns: SecurityConcern[];
}

export interface AnalyzeResponse {
    review_id: string;
    code: string;
    language: string;
    analysis: Analysis;
    created_at: string;
}

export interface DocumentRequest {
    code: string;
    language: string;
    filename?: string;
    doc_style?: string;
    llm_provider?: string;
}

export interface FunctionDoc {
    name: string;
    description: string;
    parameters: Array<{
        name: string;
        type: string;
        description: string;
    }>;
    returns: {
        type: string;
        description: string;
    };
    examples: string[];
}

export interface ClassDoc {
    name: string;
    description: string;
    attributes: Array<{
        name: string;
        type: string;
        description: string;
    }>;
    methods: FunctionDoc[];
}

export interface Documentation {
    overview: string;
    functions: FunctionDoc[];
    classes: ClassDoc[];
    usage_examples: string[];
}

export interface DocumentResponse {
    doc_id: string;
    code: string;
    language: string;
    documentation: Documentation;
    created_at: string;
}

export interface ReviewSummary {
    review_id: string;
    language: string;
    quality_score?: number;
    created_at: string;
    filename?: string;
}

export interface ReviewsListResponse {
    reviews: ReviewSummary[];
    pagination: {
        page: number;
        limit: number;
        total: number;
        pages: number;
    };
}

export interface LLMProvider {
    id: string;
    name: string;
    models: string[];
    default: boolean;
}

// API functions
export const analyzeCode = async (data: AnalyzeRequest): Promise<AnalyzeResponse> => {
    const response = await api.post('/api/analyze', data);
    return response.data;
};

export const generateDocumentation = async (data: DocumentRequest): Promise<DocumentResponse> => {
    const response = await api.post('/api/document', data);
    return response.data;
};

export const getReviews = async (page = 1, limit = 10, language?: string): Promise<ReviewsListResponse> => {
    const params = new URLSearchParams({ page: page.toString(), limit: limit.toString() });
    if (language) params.append('language', language);
    const response = await api.get(`/api/reviews?${params}`);
    return response.data;
};

export const getReview = async (reviewId: string): Promise<AnalyzeResponse> => {
    const response = await api.get(`/api/reviews/${reviewId}`);
    return response.data;
};

export const deleteReview = async (reviewId: string): Promise<void> => {
    await api.delete(`/api/reviews/${reviewId}`);
};

export const getLLMProviders = async (): Promise<{ providers: LLMProvider[] }> => {
    const response = await api.get('/api/config/llm-providers');
    return response.data;
};

export const healthCheck = async () => {
    const response = await api.get('/api/health');
    return response.data;
};
