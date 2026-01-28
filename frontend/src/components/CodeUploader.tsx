'use client';

import { useState } from 'react';
import type { AnalyzeRequest, DocumentRequest, LLMProvider } from '@/lib/api';

interface CodeUploaderProps {
    onAnalyze: (data: AnalyzeRequest) => void;
    onDocument: (data: DocumentRequest) => void;
    isAnalyzing: boolean;
    isDocumenting: boolean;
    activeTab: 'analyze' | 'document';
    providers: LLMProvider[];
}

const LANGUAGES = [
    'python', 'javascript', 'typescript', 'java', 'go',
    'rust', 'cpp', 'csharp', 'ruby', 'php'
];

const DOC_STYLES = ['google', 'numpy', 'sphinx', 'jsdoc', 'javadoc'];

export default function CodeUploader({
    onAnalyze,
    onDocument,
    isAnalyzing,
    isDocumenting,
    activeTab,
    providers,
}: CodeUploaderProps) {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');
    const [filename, setFilename] = useState('');
    const [llmProvider, setLlmProvider] = useState('gemini');
    const [docStyle, setDocStyle] = useState('google');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!code.trim()) {
            alert('Please enter some code');
            return;
        }

        const baseData = {
            code,
            language,
            filename: filename || undefined,
            llm_provider: llmProvider,
        };

        if (activeTab === 'analyze') {
            onAnalyze(baseData);
        } else {
            onDocument({ ...baseData, doc_style: docStyle });
        }
    };

    const isLoading = isAnalyzing || isDocumenting;

    return (
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8">
            <h3 className="text-2xl font-bold text-white mb-6">
                {activeTab === 'analyze' ? '📝 Code Review' : '📚 Documentation Generator'}
            </h3>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Code Input */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Your Code
                    </label>
                    <textarea
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        placeholder="Paste your code here..."
                        className="w-full h-64 px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent font-mono text-sm resize-none"
                        disabled={isLoading}
                    />
                </div>

                {/* Language Selection */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Language
                        </label>
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            disabled={isLoading}
                        >
                            {LANGUAGES.map((lang) => (
                                <option key={lang} value={lang} className="bg-slate-800">
                                    {lang.charAt(0).toUpperCase() + lang.slice(1)}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Filename (optional)
                        </label>
                        <input
                            type="text"
                            value={filename}
                            onChange={(e) => setFilename(e.target.value)}
                            placeholder="example.py"
                            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            disabled={isLoading}
                        />
                    </div>
                </div>

                {/* LLM Provider Selection */}
                {providers.length > 0 && (
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            AI Model
                        </label>
                        <select
                            value={llmProvider}
                            onChange={(e) => setLlmProvider(e.target.value)}
                            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            disabled={isLoading}
                        >
                            {providers.map((provider) => (
                                <option key={provider.id} value={provider.id} className="bg-slate-800">
                                    {provider.name} {provider.default && '(Default)'}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Doc Style (only for documentation) */}
                {activeTab === 'document' && (
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Documentation Style
                        </label>
                        <select
                            value={docStyle}
                            onChange={(e) => setDocStyle(e.target.value)}
                            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            disabled={isLoading}
                        >
                            {DOC_STYLES.map((style) => (
                                <option key={style} value={style} className="bg-slate-800">
                                    {style.charAt(0).toUpperCase() + style.slice(1)}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-4 px-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                    {isLoading ? (
                        <span className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Processing...
                        </span>
                    ) : (
                        activeTab === 'analyze' ? '🔍 Analyze Code' : '📖 Generate Documentation'
                    )}
                </button>
            </form>
        </div>
    );
}
