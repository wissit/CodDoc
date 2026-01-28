'use client';

import type { AnalyzeResponse } from '@/lib/api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface ReviewDisplayProps {
    result: AnalyzeResponse;
}

const severityColors = {
    critical: 'bg-red-500/20 border-red-500/50 text-red-300',
    high: 'bg-orange-500/20 border-orange-500/50 text-orange-300',
    medium: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-300',
    low: 'bg-blue-500/20 border-blue-500/50 text-blue-300',
    info: 'bg-gray-500/20 border-gray-500/50 text-gray-300',
};

const priorityColors = {
    high: 'text-red-400',
    medium: 'text-yellow-400',
    low: 'text-blue-400',
};

export default function ReviewDisplay({ result }: ReviewDisplayProps) {
    const { analysis } = result;

    return (
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <h3 className="text-2xl font-bold text-white">Code Review Results</h3>
                <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-400">Quality Score:</span>
                    <span className={`text-2xl font-bold ${analysis.quality_score >= 8 ? 'text-green-400' :
                            analysis.quality_score >= 6 ? 'text-yellow-400' :
                                'text-red-400'
                        }`}>
                        {analysis.quality_score.toFixed(1)}/10
                    </span>
                </div>
            </div>

            {/* Summary */}
            <div className="bg-black/30 rounded-lg p-4 border border-white/10">
                <h4 className="text-lg font-semibold text-white mb-2">Summary</h4>
                <p className="text-gray-300">{analysis.summary}</p>
            </div>

            {/* Security Concerns */}
            {analysis.security_concerns && analysis.security_concerns.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">🔒 Security Concerns</h4>
                    <div className="space-y-3">
                        {analysis.security_concerns.map((concern, index) => (
                            <div
                                key={index}
                                className={`p-4 rounded-lg border ${severityColors[concern.severity]}`}
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <h5 className="font-semibold">{concern.title}</h5>
                                    <span className="text-xs uppercase px-2 py-1 rounded bg-black/30">
                                        {concern.severity}
                                    </span>
                                </div>
                                <p className="text-sm mb-2">{concern.description}</p>
                                <div className="bg-black/30 rounded p-2 text-sm">
                                    <strong>Recommendation:</strong> {concern.recommendation}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Issues */}
            {analysis.issues && analysis.issues.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">⚠️ Issues Found</h4>
                    <div className="space-y-3">
                        {analysis.issues.map((issue, index) => (
                            <div
                                key={index}
                                className={`p-4 rounded-lg border ${severityColors[issue.severity]}`}
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <div>
                                        <span className="text-xs uppercase px-2 py-1 rounded bg-black/30 mr-2">
                                            {issue.severity}
                                        </span>
                                        <span className="text-xs uppercase px-2 py-1 rounded bg-black/30">
                                            {issue.category}
                                        </span>
                                    </div>
                                    {issue.line_number && (
                                        <span className="text-xs text-gray-400">Line {issue.line_number}</span>
                                    )}
                                </div>
                                <p className="text-sm mb-2">{issue.description}</p>
                                {issue.suggestion && (
                                    <div className="bg-black/30 rounded p-2 text-sm">
                                        <strong>Suggestion:</strong> {issue.suggestion}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Suggestions */}
            {analysis.suggestions && analysis.suggestions.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">💡 Suggestions</h4>
                    <div className="space-y-3">
                        {analysis.suggestions.map((suggestion, index) => (
                            <div
                                key={index}
                                className="p-4 rounded-lg border border-white/10 bg-black/20"
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <h5 className="font-semibold text-white">{suggestion.title}</h5>
                                    <span className={`text-xs uppercase ${priorityColors[suggestion.priority]}`}>
                                        {suggestion.priority} priority
                                    </span>
                                </div>
                                <p className="text-sm text-gray-300 mb-2">{suggestion.description}</p>
                                {suggestion.code_example && (
                                    <div className="mt-2">
                                        <p className="text-xs text-gray-400 mb-1">Example:</p>
                                        <SyntaxHighlighter
                                            language={result.language}
                                            style={vscDarkPlus}
                                            customStyle={{
                                                margin: 0,
                                                borderRadius: '0.5rem',
                                                fontSize: '0.875rem',
                                            }}
                                        >
                                            {suggestion.code_example}
                                        </SyntaxHighlighter>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Original Code */}
            <div>
                <h4 className="text-lg font-semibold text-white mb-3">📄 Analyzed Code</h4>
                <SyntaxHighlighter
                    language={result.language}
                    style={vscDarkPlus}
                    customStyle={{
                        borderRadius: '0.75rem',
                        fontSize: '0.875rem',
                    }}
                    showLineNumbers
                >
                    {result.code}
                </SyntaxHighlighter>
            </div>
        </div>
    );
}
