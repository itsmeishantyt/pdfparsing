import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
const pdf = require('pdf-parse');

const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
);

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;
        const metadataStr = formData.get('metadata') as string;

        if (!file) {
            return NextResponse.json({ detail: 'No file provided' }, { status: 400 });
        }

        const metadata = JSON.parse(metadataStr);

        // Convert file to buffer
        const arrayBuffer = await file.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);

        // Parse PDF
        const startTime = Date.now();
        const pdfData = await pdf(buffer);

        // Simple text-based question extraction
        const questions = extractQuestions(pdfData.text);

        // Store in database
        const paperId = await storePaper(metadata, questions);

        const processingTime = (Date.now() - startTime) / 1000;

        return NextResponse.json({
            paperId,
            status: 'success',
            questionsCount: questions.length,
            processingTime,
            message: `Successfully parsed ${questions.length} questions`
        });

    } catch (error: any) {
        console.error('Error processing PDF:', error);
        return NextResponse.json(
            { detail: `Error processing PDF: ${error.message}` },
            { status: 500 }
        );
    }
}

function extractQuestions(text: string): any[] {
    // Split by question numbers (1, 2, 3, etc.)
    const questionPattern = /(?:^|\n)(\d+)[\s.)]+(.*?)(?=\n\d+[\s.)]|$)/g;
    const questions: any[] = [];
    let match;
    let order = 0;

    while ((match = questionPattern.exec(text)) !== null) {
        const questionNumber = match[1];
        const content = match[2].trim();

        // Try to extract marks
        const marksMatch = content.match(/\[?(\d+)\s*marks?\]?/i);
        const marks = marksMatch ? parseInt(marksMatch[1]) : null;

        questions.push({
            questionNumber,
            sequenceOrder: order++,
            content,
            marks
        });
    }

    return questions;
}

async function storePaper(metadata: any, questions: any[]): Promise<string> {
    const paperId = crypto.randomUUID();

    const title = `${metadata.examBoard} ${metadata.subject || 'Economics'} ${metadata.level || 'A-Level'} Paper ${metadata.paperNumber} - ${metadata.session} ${metadata.year}`;

    // Insert paper
    await supabase.from('Paper').insert({
        id: paperId,
        title,
        exam_board: metadata.examBoard,
        subject: metadata.subject || 'Economics',
        level: metadata.level || 'A-Level',
        year: metadata.year,
        session: metadata.session,
        paper_number: metadata.paperNumber,
        total_marks: metadata.totalMarks,
        uploaded_at: new Date().toISOString()
    });

    // Insert questions
    for (const question of questions) {
        const questionId = crypto.randomUUID();

        await supabase.from('Question').insert({
            id: questionId,
            paper_id: paperId,
            question_number: question.questionNumber,
            sequence_order: question.sequenceOrder,
            marks: question.marks
        });

        // Insert text content
        await supabase.from('QuestionContent').insert({
            id: crypto.randomUUID(),
            question_id: questionId,
            sequence_order: 0,
            content_type: 'TEXT',
            text: question.content
        });
    }

    return paperId;
}
