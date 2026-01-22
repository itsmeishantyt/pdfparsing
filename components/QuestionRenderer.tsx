/**
 * Component for rendering a complete question with all its content.
 * Displays question number, marks, and content elements in order.
 */
import React from 'react';
import ContentElement, { QuestionContent } from './ContentElement';

export interface Question {
    id: string;
    questionNumber: string;
    sequenceOrder: number;
    marks?: number;
    content: QuestionContent[];
}

interface QuestionRendererProps {
    question: Question;
    preserveLayout?: boolean;
}

export default function QuestionRenderer({
    question,
    preserveLayout = false
}: QuestionRendererProps) {
    return (
        <div className="question-container">
            <div className="question-header">
                <span className="question-number">
                    Question {question.questionNumber}
                </span>
                {question.marks && (
                    <span className="marks">[{question.marks} marks]</span>
                )}
            </div>

            <div className="question-content">
                {question.content
                    .sort((a, b) => a.sequenceOrder - b.sequenceOrder)
                    .map((item) => (
                        <ContentElement
                            key={item.id}
                            content={item}
                            preserveLayout={preserveLayout}
                        />
                    ))}
            </div>
        </div>
    );
}
