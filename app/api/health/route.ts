import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json({
        status: 'healthy',
        service: 'PDF Parsing API',
        runtime: 'Next.js'
    });
}
