'use client';

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { analyzeCode, generateDocumentation, getLLMProviders, type AnalyzeRequest, type DocumentRequest } from '@/lib/api';
import CodeUploader from '@/components/CodeUploader';
import ReviewDisplay from '@/components/ReviewDisplay';
import DocumentationViewer from '@/components/DocumentationViewer';
import Link from 'next/link';

export default function Home() {
    const [activeTab, setActiveTab] = useState<'analyze' | 'document'>('analyze');
    const [analyzeResult, setAnalyzeResult] = useState<any>(null);
    const [docResult, setDocResult] = useState<any>(null);

    const { data: providersData } = useQuery({
        queryKey: ['llm-providers'],
        queryFn: getLLMProviders,
    });

    const analyzeMutation = useMutation({
        mutationFn: analyzeCode,
        onSuccess: (data) => {
            setAnalyzeResult(data);
        },
    });

    const documentMutation = useMutation({
        mutationFn: generateDocumentation,
        onSuccess: (data) => {
            setDocResult(data);
        },
    });

    const handleAnalyze = (data: AnalyzeRequest) => {
        setAnalyzeResult(null);
        analyzeMutation.mutate(data);
    };

    const handleDocument = (data: DocumentRequest) => {
        setDocResult(null);
        documentMutation.mutate(data);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <header className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
                <div className="container mx-auto px-4 py-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                                <span className="text-white font-bold text-xl">C</span>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white">CodDoc AI</h1>
                                <p className="text-sm text-gray-400">AI-Powered Code Assistant</p>
                            </div>
                        </div>
                        <nav className="flex items-center space-x-6">
                            <Link href="/history" className="text-gray-300 hover:text-white transition-colors">
                                History
                            </Link>
                            <a
                                href={`${process.env.NEXT_PUBLIC_API_URL}/docs`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-gray-300 hover:text-white transition-colors"
                            >
                                API Docs
                            </a>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-12">
                {/* Hero Section */}
                <div className="text-center mb-12 animate-fade-in">
                    <h2 className="text-5xl font-bold text-white mb-4">
                        Transform Your Code with AI
                    </h2>
                    <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                        Get instant code reviews, security analysis, and comprehensive documentation
                        powered by advanced AI models
                    </p>
                    {providersData && (
                        <div className="mt-4 flex items-center justify-center space-x-2">
                            <span className="text-sm text-gray-400">Powered by:</span>
                            {providersData.providers.map((provider) => (
                                <span
                                    key={provider.id}
                                    className={`text-sm px-3 py-1 rounded-full ${provider.default
                                            ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                                            : 'bg-gray-700/20 text-gray-400'
                                        }`}
                                >
                                    {provider.name}
                                </span>
                            ))}
                        </div>
                    )}
                </div>

                {/* Tabs */}
                <div className="flex justify-center mb-8">
                    <div className="inline-flex rounded-lg bg-black/30 p-1 backdrop-blur-sm">
                        <button
                            onClick={() => setActiveTab('analyze')}
                            className={`px-8 py-3 rounded-lg font-medium transition-all ${activeTab === 'analyze'
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                                    : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Code Review
                        </button>
                        <button
                            onClick={() => setActiveTab('document')}
                            className={`px-8 py-3 rounded-lg font-medium transition-all ${activeTab === 'document'
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                                    : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Generate Docs
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Column - Input */}
                    <div className="animate-slide-up">
                        <CodeUploader
                            onAnalyze={handleAnalyze}
                            onDocument={handleDocument}
                            isAnalyzing={analyzeMutation.isPending}
                            isDocumenting={documentMutation.isPending}
                            activeTab={activeTab}
                            providers={providersData?.providers || []}
                        />
                    </div>

                    {/* Right Column - Results */}
                    <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
                        {activeTab === 'analyze' && (
                            <>
                                {analyzeMutation.isPending && (
                                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center">
                                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mb-4"></div>
                                        <p className="text-gray-300">Analyzing your code...</p>
                                    </div>
                                )}
                                {analyzeMutation.isError && (
                                    <div className="bg-red-500/10 backdrop-blur-lg rounded-2xl border border-red-500/30 p-6">
                                        <p className="text-red-300">
                                            Error: {(analyzeMutation.error as Error).message}
                                        </p>
                                    </div>
                                )}
                                {analyzeResult && <ReviewDisplay result={analyzeResult} />}
                                {!analyzeMutation.isPending && !analyzeResult && !analyzeMutation.isError && (
                                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center">
                                        <div className="text-6xl mb-4">🔍</div>
                                        <p className="text-gray-400">Your code review will appear here</p>
                                    </div>
                                )}
                            </>
                        )}

                        {activeTab === 'document' && (
                            <>
                                {documentMutation.isPending && (
                                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center">
                                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mb-4"></div>
                                        <p className="text-gray-300">Generating documentation...</p>
                                    </div>
                                )}
                                {documentMutation.isError && (
                                    <div className="bg-red-500/10 backdrop-blur-lg rounded-2xl border border-red-500/30 p-6">
                                        <p className="text-red-300">
                                            Error: {(documentMutation.error as Error).message}
                                        </p>
                                    </div>
                                )}
                                {docResult && <DocumentationViewer result={docResult} />}
                                {!documentMutation.isPending && !docResult && !documentMutation.isError && (
                                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center">
                                        <div className="text-6xl mb-4">📚</div>
                                        <p className="text-gray-400">Your documentation will appear here</p>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                </div>

                {/* Features Section */}
                <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 card-hover">
                        <div className="text-4xl mb-4">⚡</div>
                        <h3 className="text-xl font-bold text-white mb-2">Instant Analysis</h3>
                        <p className="text-gray-400">
                            Get comprehensive code reviews in seconds with AI-powered insights
                        </p>
                    </div>
                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 card-hover">
                        <div className="text-4xl mb-4">🔒</div>
                        <h3 className="text-xl font-bold text-white mb-2">Security First</h3>
                        <p className="text-gray-400">
                            Identify security vulnerabilities and get actionable recommendations
                        </p>
                    </div>
                    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 card-hover">
                        <div className="text-4xl mb-4">📖</div>
                        <h3 className="text-xl font-bold text-white mb-2">Auto Documentation</h3>
                        <p className="text-gray-400">
                            Generate professional documentation automatically for your codebase
                        </p>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="border-t border-white/10 bg-black/20 backdrop-blur-lg mt-20">
                <div className="container mx-auto px-4 py-8 text-center text-gray-400">
                    <p>© 2024 CodDoc AI. Powered by advanced AI models.</p>
                </div>
            </footer>
        </div>
    );
}
