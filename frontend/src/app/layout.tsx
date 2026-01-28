import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { QueryProvider } from '@/components/QueryProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'CodDoc AI - AI-Powered Code Review & Documentation',
    description: 'Automatically generate code reviews and documentation using AI',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <QueryProvider>
                    {children}
                </QueryProvider>
            </body>
        </html>
    )
}
