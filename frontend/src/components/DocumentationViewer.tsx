'use client';

import type { DocumentResponse } from '@/lib/api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ReactMarkdown from 'react-markdown';

interface DocumentationViewerProps {
    result: DocumentResponse;
}

export default function DocumentationViewer({ result }: DocumentationViewerProps) {
    const { documentation } = result;

    return (
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 space-y-6">
            {/* Header */}
            <div>
                <h3 className="text-2xl font-bold text-white mb-2">Documentation</h3>
                <p className="text-sm text-gray-400">
                    Generated for {result.language} • {new Date(result.created_at).toLocaleString()}
                </p>
            </div>

            {/* Overview */}
            {documentation.overview && (
                <div className="bg-black/30 rounded-lg p-4 border border-white/10">
                    <h4 className="text-lg font-semibold text-white mb-2">📖 Overview</h4>
                    <p className="text-gray-300">{documentation.overview}</p>
                </div>
            )}

            {/* Functions */}
            {documentation.functions && documentation.functions.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">⚡ Functions</h4>
                    <div className="space-y-4">
                        {documentation.functions.map((func, index) => (
                            <div
                                key={index}
                                className="bg-black/20 rounded-lg p-4 border border-white/10"
                            >
                                <h5 className="text-lg font-mono text-purple-400 mb-2">{func.name}()</h5>
                                <p className="text-gray-300 mb-3">{func.description}</p>

                                {/* Parameters */}
                                {func.parameters && func.parameters.length > 0 && (
                                    <div className="mb-3">
                                        <p className="text-sm font-semibold text-gray-400 mb-2">Parameters:</p>
                                        <div className="space-y-2">
                                            {func.parameters.map((param, pIndex) => (
                                                <div key={pIndex} className="bg-black/30 rounded p-2 text-sm">
                                                    <span className="font-mono text-blue-400">{param.name}</span>
                                                    <span className="text-gray-500 mx-2">:</span>
                                                    <span className="text-green-400">{param.type}</span>
                                                    <p className="text-gray-400 mt-1">{param.description}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Returns */}
                                {func.returns && (
                                    <div className="mb-3">
                                        <p className="text-sm font-semibold text-gray-400 mb-2">Returns:</p>
                                        <div className="bg-black/30 rounded p-2 text-sm">
                                            <span className="text-green-400">{func.returns.type}</span>
                                            <p className="text-gray-400 mt-1">{func.returns.description}</p>
                                        </div>
                                    </div>
                                )}

                                {/* Examples */}
                                {func.examples && func.examples.length > 0 && (
                                    <div>
                                        <p className="text-sm font-semibold text-gray-400 mb-2">Examples:</p>
                                        {func.examples.map((example, eIndex) => (
                                            <SyntaxHighlighter
                                                key={eIndex}
                                                language={result.language}
                                                style={vscDarkPlus}
                                                customStyle={{
                                                    margin: '0.5rem 0',
                                                    borderRadius: '0.5rem',
                                                    fontSize: '0.875rem',
                                                }}
                                            >
                                                {example}
                                            </SyntaxHighlighter>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Classes */}
            {documentation.classes && documentation.classes.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">🏗️ Classes</h4>
                    <div className="space-y-4">
                        {documentation.classes.map((cls, index) => (
                            <div
                                key={index}
                                className="bg-black/20 rounded-lg p-4 border border-white/10"
                            >
                                <h5 className="text-lg font-mono text-pink-400 mb-2">{cls.name}</h5>
                                <p className="text-gray-300 mb-3">{cls.description}</p>

                                {/* Attributes */}
                                {cls.attributes && cls.attributes.length > 0 && (
                                    <div className="mb-3">
                                        <p className="text-sm font-semibold text-gray-400 mb-2">Attributes:</p>
                                        <div className="space-y-2">
                                            {cls.attributes.map((attr, aIndex) => (
                                                <div key={aIndex} className="bg-black/30 rounded p-2 text-sm">
                                                    <span className="font-mono text-blue-400">{attr.name}</span>
                                                    <span className="text-gray-500 mx-2">:</span>
                                                    <span className="text-green-400">{attr.type}</span>
                                                    <p className="text-gray-400 mt-1">{attr.description}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Methods */}
                                {cls.methods && cls.methods.length > 0 && (
                                    <div>
                                        <p className="text-sm font-semibold text-gray-400 mb-2">Methods:</p>
                                        <div className="space-y-2">
                                            {cls.methods.map((method, mIndex) => (
                                                <div key={mIndex} className="bg-black/30 rounded p-2 text-sm">
                                                    <span className="font-mono text-purple-400">{method.name}()</span>
                                                    <p className="text-gray-400 mt-1">{method.description}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Usage Examples */}
            {documentation.usage_examples && documentation.usage_examples.length > 0 && (
                <div>
                    <h4 className="text-lg font-semibold text-white mb-3">💻 Usage Examples</h4>
                    <div className="space-y-3">
                        {documentation.usage_examples.map((example, index) => (
                            <SyntaxHighlighter
                                key={index}
                                language={result.language}
                                style={vscDarkPlus}
                                customStyle={{
                                    borderRadius: '0.75rem',
                                    fontSize: '0.875rem',
                                }}
                            >
                                {example}
                            </SyntaxHighlighter>
                        ))}
                    </div>
                </div>
            )}

            {/* Original Code */}
            <div>
                <h4 className="text-lg font-semibold text-white mb-3">📄 Original Code</h4>
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
