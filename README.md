Whatever code you write must be scalable must not break under load and should be working dont use imaginary apis etcc always act as an experienced developer dont hallucinate ask me if necessary

# Economics A-Level Past Paper Parsing System

✅ **Ready for FREE deployment to Vercel!**

This system parses Economics A-level past paper PDFs and displays them with 1:1 accuracy in a web interface.

## Quick Start

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
# Copy .env.example to .env.local
cp .env.example .env.local

# For local development, add to .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=your_supabase_postgres_url
```

3. Run the development server:
```bash
npm run dev
```

Visit `http://localhost:3000`

### Deploy to Vercel (Free Forever)

🚀 **See [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) for complete deployment guide**

Quick steps:
1. Push code to GitHub
2. Import to Vercel
3. Add environment variables (Supabase credentials)
4. Deploy!

Your app will be live at `your-project.vercel.app` with both frontend and backend**FREE FOREVER**.

## Features

- 📄 PDF parsing with text and image extraction
- 🎯 Intelligent question segmentation
- 📐 Layout preservation for 1:1 reproduction
- 🖼️ Image and diagram extraction
- 📱 Responsive, modern UI
- 🚀 Free forever hosting on Vercel

## Tech Stack (100% Free)

- **Frontend**: Next.js 14, React, TypeScript
- **Backend**: Python serverless functions on Vercel
- **Database**: Supabase PostgreSQL (free tier)
- **Storage**: Supabase Storage (free tier)
- **Hosting**: Vercel (free forever)

## Documentation

- [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) - Complete deployment guide
- [SETUP.md](SETUP.md) - Detailed setup and configuration
- [walkthrough.md](.gemini/antigravity/brain/.../walkthrough.md) - System architecture

---

Built with 100% free and open-source technologies 🎉