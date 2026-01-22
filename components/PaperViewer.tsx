/**
 * Component for rendering a complete paper with all questions.
 */
import React from 'react';
import QuestionRenderer, { Question } from './QuestionRenderer';

export interface Paper {
    id: string;
    title: string;
    examBoard: string;
    subject: string;
    level: string;
    year: number;
    session: string;
    paperNumber: number;
    totalMarks?: number;
    uploadedAt: string;
    questions: Question[];
}

interface PaperViewerProps {
    paper: Paper;
    preserveLayout?: boolean;
}

export default function PaperViewer({
    paper,
    preserveLayout = false
}: PaperViewerProps) {
    return (
        <div className="paper-viewer">
            <div className="paper-header">
                <h1 className="paper-title">{paper.title}</h1>
                <div className="paper-metadata">
                    <span>{paper.examBoard} | {paper.subject} | {paper.level}</span>
                    <span>{paper.session} {paper.year} - Paper {paper.paperNumber}</span>
                    {paper.totalMarks && (
                        <span className="total-marks">Total: {paper.totalMarks} marks</span>
                    )}
                </div>
            </div>

            <div className="questions-list">
                {paper.questions
                    .sort((a, b) => a.sequenceOrder - b.sequenceOrder)
                    .map((question) => (
                        <QuestionRenderer
                            key={question.id}
                            question={question}
                            preserveLayout={preserveLayout}
                        />
                    ))}
            </div>
        </div>
    );
}
