import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
);

export async function GET(
    request: NextRequest,
    { params }: { params: { paperId: string } }
) {
    try {
        const { paperId } = params;

        // Get paper
        const { data: paper, error: paperError } = await supabase
            .from('Paper')
            .select('*')
            .eq('id', paperId)
            .single();

        if (paperError || !paper) {
            return NextResponse.json(
                { detail: `Paper ${paperId} not found` },
                { status: 404 }
            );
        }

        // Get questions
        const { data: questions } = await supabase
            .from('Question')
            .select('*')
            .eq('paper_id', paperId)
            .order('sequence_order');

        // Get content for each question
        for (const question of questions || []) {
            const { data: content } = await supabase
                .from('QuestionContent')
                .select('*')
                .eq('question_id', question.id)
                .order('sequence_order');

            question.content = content;
        }

        paper.questions = questions;

        return NextResponse.json(paper);

    } catch (error: any) {
        console.error('Error retrieving paper:', error);
        return NextResponse.json(
            { detail: `Error retrieving paper: ${error.message}` },
            { status: 500 }
        );
    }
}
