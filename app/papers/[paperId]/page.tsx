'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import PaperViewer from '@/components/PaperViewer';
import { getPaper } from '@/lib/api';
import type { Paper } from '@/components/PaperViewer';

export default function PaperPage() {
    const params = useParams();
    const paperId = params.paperId as string;

    const [paper, setPaper] = useState<Paper | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadPaper() {
            try {
                setLoading(true);
                const data = await getPaper(paperId);
                setPaper(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load paper');
            } finally {
                setLoading(false);
            }
        }

        if (paperId) {
            loadPaper();
        }
    }, [paperId]);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading past paper...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>Error</h2>
                <p>{error}</p>
                <a href="/" className="btn-primary">Go Home</a>
            </div>
        );
    }

    if (!paper) {
        return (
            <div className="error-container">
                <h2>Paper Not Found</h2>
                <a href="/" className="btn-primary">Go Home</a>
            </div>
        );
    }

    return (
        <main className="paper-page">
            <PaperViewer paper={paper} />
        </main>
    );
}
