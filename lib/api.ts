/**
 * API client for interacting with the parsing backend.
 */

// For Vercel: backend and frontend on same domain, use relative paths
// For local dev: backend on different port
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export interface PaperMetadata {
    examBoard: string;
    subject?: string;
    level?: string;
    year: number;
    session: string;
    paperNumber: number;
    totalMarks?: number;
    title?: string;
}

export interface ParseResponse {
    paperId: string;
    status: string;
    questionsCount: number;
    processingTime: number;
    message?: string;
}

/**
 * Upload and parse a PDF file.
 */
export async function uploadPDF(
    file: File,
    metadata: PaperMetadata
): Promise<ParseResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    const response = await fetch(`${API_BASE_URL}/api/parse/upload`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to upload PDF');
    }

    return response.json();
}

/**
 * Fetch a parsed paper by ID.
 */
export async function getPaper(paperId: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/parse/papers/${paperId}`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch paper');
    }

    return response.json();
}

/**
 * Check API health.
 */
export async function checkHealth(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/parse/health`);
        return response.ok;
    } catch {
        return false;
    }
}
