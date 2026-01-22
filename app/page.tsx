'use client';

import { useState } from 'react';
import { uploadPDF, type PaperMetadata } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Home() {
    const router = useRouter();
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [metadata, setMetadata] = useState<PaperMetadata>({
        examBoard: 'AQA',
        subject: 'Economics',
        level: 'A-Level',
        year: new Date().getFullYear(),
        session: 'June',
        paperNumber: 1,
    });

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            if (!selectedFile.name.endsWith('.pdf')) {
                setError('Please select a PDF file');
                return;
            }
            setFile(selectedFile);
            setError(null);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError('Please select a file');
            return;
        }

        setUploading(true);
        setError(null);

        try {
            const result = await uploadPDF(file, metadata);
            console.log('Upload successful:', result);

            // Redirect to paper view
            router.push(`/papers/${result.paperId}`);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    return (
        <main className="home-page">
            <div className="container">
                <h1>Economics Past Paper Parser</h1>
                <p className="subtitle">
                    Upload A-Level Economics past papers to parse and view questions
                </p>

                <div className="upload-card">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="file-upload" className="file-label">
                                Select PDF File
                            </label>
                            <input
                                id="file-upload"
                                type="file"
                                accept=".pdf"
                                onChange={handleFileChange}
                                className="file-input"
                            />
                            {file && <p className="file-name">{file.name}</p>}
                        </div>

                        <div className="metadata-grid">
                            <div className="form-group">
                                <label>Exam Board</label>
                                <select
                                    value={metadata.examBoard}
                                    onChange={(e) => setMetadata({ ...metadata, examBoard: e.target.value })}
                                    className="select-input"
                                >
                                    <option value="AQA">AQA</option>
                                    <option value="Edexcel">Edexcel</option>
                                    <option value="OCR">OCR</option>
                                    <option value="WJEC">WJEC</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Year</label>
                                <input
                                    type="number"
                                    value={metadata.year}
                                    onChange={(e) => setMetadata({ ...metadata, year: parseInt(e.target.value) })}
                                    min="2000"
                                    max="2030"
                                    className="text-input"
                                />
                            </div>

                            <div className="form-group">
                                <label>Session</label>
                                <select
                                    value={metadata.session}
                                    onChange={(e) => setMetadata({ ...metadata, session: e.target.value })}
                                    className="select-input"
                                >
                                    <option value="June">June</option>
                                    <option value="November">November</option>
                                    <option value="January">January</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Paper Number</label>
                                <input
                                    type="number"
                                    value={metadata.paperNumber}
                                    onChange={(e) => setMetadata({ ...metadata, paperNumber: parseInt(e.target.value) })}
                                    min="1"
                                    max="3"
                                    className="text-input"
                                />
                            </div>
                        </div>

                        {error && <div className="error-message">{error}</div>}

                        <button
                            type="submit"
                            disabled={!file || uploading}
                            className="btn-primary"
                        >
                            {uploading ? 'Uploading...' : 'Upload & Parse PDF'}
                        </button>
                    </form>
                </div>
            </div>
        </main>
    );
}
