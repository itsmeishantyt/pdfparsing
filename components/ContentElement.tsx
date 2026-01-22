/**
 * Component for rendering individual content elements within a question.
 * Handles text, images, and other content types with layout preservation.
 */
import Image from 'next/image';
import React, { CSSProperties } from 'react';

export type ContentType = 'TEXT' | 'IMAGE' | 'TABLE' | 'DIAGRAM' | 'EQUATION';

export interface QuestionContent {
    id: string;
    sequenceOrder: number;
    contentType: ContentType;

    // Text content
    text?: string;
    fontSize?: number;
    fontFamily?: string;
    isBold?: boolean;
    isItalic?: boolean;

    // Layout
    x?: number;
    y?: number;
    width?: number;
    height?: number;

    // Image content
    imageUrl?: string;
    imageWidth?: number;
    imageHeight?: number;
    altText?: string;
}

interface ContentElementProps {
    content: QuestionContent;
    preserveLayout?: boolean;
}

export default function ContentElement({
    content,
    preserveLayout = false
}: ContentElementProps) {
    // Build style based on content properties
    const style: CSSProperties = {
        fontSize: content.fontSize ? `${content.fontSize}px` : undefined,
        fontFamily: content.fontFamily || undefined,
        fontWeight: content.isBold ? 'bold' : 'normal',
        fontStyle: content.isItalic ? 'italic' : 'normal',
    };

    // Add positioning if layout preservation is enabled
    if (preserveLayout && content.x !== undefined && content.y !== undefined) {
        style.position = 'absolute';
        style.left = `${content.x}px`;
        style.top = `${content.y}px`;
    }

    switch (content.contentType) {
        case 'TEXT':
            return (
                <span style={style} className="question-text">
                    {content.text}
                </span>
            );

        case 'IMAGE':
            if (!content.imageUrl) return null;

            return (
                <div style={style} className="question-image-wrapper">
                    <Image
                        src={content.imageUrl}
                        alt={content.altText || 'Question image'}
                        width={content.imageWidth || 400}
                        height={content.imageHeight || 300}
                        className="question-image"
                    />
                </div>
            );

        case 'DIAGRAM':
        case 'TABLE':
            if (content.imageUrl) {
                return (
                    <div style={style} className="question-diagram-wrapper">
                        <Image
                            src={content.imageUrl}
                            alt={content.altText || 'Diagram'}
                            width={content.imageWidth || 500}
                            height={content.imageHeight || 400}
                            className="question-image"
                        />
                    </div>
                );
            }
            return null;

        default:
            return null;
    }
}
