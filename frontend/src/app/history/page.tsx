'use client';

import { useQuery } from '@tanstack/react-query';
import { getReviews } from '@/lib/api';
import Link from 'next/link';
import { useState } from 'react';

export default function HistoryPage() {
    const [page, setPage] = useState(1);
    const [language, setLanguage] = useState('');

    const { data, isLoading, error } = useQuery({
        queryKey: ['reviews', page, language],
        queryFn: () => getReviews(page, 10, language || undefined),
    });

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <header className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
                <div className="container mx-auto px-4 py-6">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-3">
                            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                                <span className="text-white font-bold text-xl">C</span>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white">CodDoc AI</h1>
                                <p className="text-sm text-gray-400">Review History</p>
                            </div>
                        </Link>
                        <Link
                            href="/"
                            className="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
                        >
                            ← Back to Home
                        </Link>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-12">
                <div className="mb-8">
                    <h2 className="text-4xl font-bold text-white mb-4">Review History</h2>
                    <p className="text-gray-300">Browse your previous code reviews and documentation</p>
                </div>

                {/* Filters */}
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Filter by Language
                    </label>
                    <select
                        value={language}
                        onChange={(e) => {
                            setLanguage(e.target.value);
                            setPage(1);
                        }}
                        className="px-4 py-2 bg-black/30 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="" className="bg-slate-800">All Languages</option>
                        <option value="python" className="bg-slate-800">Python</option>
                        <option value="javascript" className="bg-slate-800">JavaScript</option>
                        <option value="typescript" className="bg-slate-800">TypeScript</option>
                        <option value="java" className="bg-slate-800">Java</option>
                        <option value="go" className="bg-slate-800">Go</option>
                    </select>
                </div>

                {/* Reviews List */}
                {isLoading && (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
                        <p className="text-gray-300 mt-4">Loading reviews...</p>
                    </div>
                )}

                {error && (
                    <div className="bg-red-500/10 backdrop-blur-lg rounded-2xl border border-red-500/30 p-6">
                        <p className="text-red-300">Error loading reviews: {(error as Error).message}</p>
                    </div>
                )}

                {data && (
                    <>
                        {data.reviews.length === 0 ? (
                            <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center">
                                <div className="text-6xl mb-4">📭</div>
                                <p className="text-gray-400">No reviews found</p>
                                <Link
                                    href="/"
                                    className="inline-block mt-4 px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
                                >
                                    Create Your First Review
                                </Link>
                            </div>
                        ) : (
                            <>
                                <div className="grid gap-4">
                                    {data.reviews.map((review) => (
                                        <div
                                            key={review.review_id}
                                            className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 p-6 card-hover"
                                        >
                                            <div className="flex items-center justify-between">
                                                <div className="flex-1">
                                                    <div className="flex items-center space-x-3 mb-2">
                                                        <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm">
                                                            {review.language}
                                                        </span>
                                                        {review.filename && (
                                                            <span className="text-gray-400 text-sm font-mono">
                                                                {review.filename}
                                                            </span>
                                                        )}
                                                    </div>
                                                    <p className="text-gray-400 text-sm">
                                                        {new Date(review.created_at).toLocaleString()}
                                                    </p>
                                                </div>
                                                <div className="flex items-center space-x-4">
                                                    {review.quality_score !== undefined && (
                                                        <div className="text-center">
                                                            <p className="text-xs text-gray-400 mb-1">Quality</p>
                                                            <p className={`text-2xl font-bold ${review.quality_score >= 8 ? 'text-green-400' :
                                                                    review.quality_score >= 6 ? 'text-yellow-400' :
                                                                        'text-red-400'
                                                                }`}>
                                                                {review.quality_score.toFixed(1)}
                                                            </p>
                                                        </div>
                                                    )}
                                                    <Link
                                                        href={`/review/${review.review_id}`}
                                                        className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
                                                    >
                                                        View Details →
                                                    </Link>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                {/* Pagination */}
                                {data.pagination.pages > 1 && (
                                    <div className="mt-8 flex items-center justify-center space-x-4">
                                        <button
                                            onClick={() => setPage(p => Math.max(1, p - 1))}
                                            disabled={page === 1}
                                            className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white/10 transition-colors"
                                        >
                                            ← Previous
                                        </button>
                                        <span className="text-gray-300">
                                            Page {page} of {data.pagination.pages}
                                        </span>
                                        <button
                                            onClick={() => setPage(p => Math.min(data.pagination.pages, p + 1))}
                                            disabled={page === data.pagination.pages}
                                            className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white/10 transition-colors"
                                        >
                                            Next →
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                    </>
                )}
            </main>
        </div>
    );
}
