# 🚀 Deploying to Vercel (Free Forever)

This guide will help you deploy both the frontend and backend to Vercel for completely free hosting.

## Prerequisites

1. GitHub account
2. Vercel account (sign up at [vercel.com](https://vercel.com))
3. Supabase project with database tables created

## Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - PDF parsing system"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/parsing-project.git
git push -u origin main
```

## Step 2: Import Project to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your GitHub repository
4. Vercel will auto-detect Next.js configuration

## Step 3: Configure Environment Variables

In the Vercel dashboard, add these environment variables:

### Required Variables

```
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=your_anon_public_key
SUPABASE_SERVICE_KEY=your_service_role_secret_key
STORAGE_BUCKET=question-images
```

### How to Get Supabase Credentials

1. Go to your Supabase project dashboard
2. Click **Settings** → **API**
3. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon/public** key → `SUPABASE_KEY`
   - **service_role** key → `SUPABASE_SERVICE_KEY`
4. Click **Settings** → **Database**
5. Copy **Connection string** → `DATABASE_URL`
   - Make sure to replace `[YOUR-PASSWORD]` with your actual database password

## Step 4: Deploy

1. Click "Deploy"
2. Vercel will:
   - Install dependencies
   - Build the Next.js frontend
   - Deploy Python serverless functions from `/api` folder
   - Generate a production URL (e.g., `your-project.vercel.app`)

**First deployment takes 2-3 minutes**

## Step 5: Setup Database Tables

After deployment, you need to create the database tables:

### Option A: Using Prisma (Recommended)

```bash
# Install dependencies locally
npm install

# Push schema to Supabase
npx prisma db push
```

### Option B: Using Supabase SQL Editor

Go to Supabase → SQL Editor and run:

```sql
-- Create ContentType enum
CREATE TYPE "ContentType" AS ENUM ('TEXT', 'IMAGE', 'TABLE', 'DIAGRAM', 'EQUATION');

-- Create Paper table
CREATE TABLE "Paper" (
    "id" TEXT PRIMARY KEY,
    "title" TEXT NOT NULL,
    "exam_board" TEXT NOT NULL,
    "subject" TEXT NOT NULL,
    "level" TEXT NOT NULL,
    "year" INTEGER NOT NULL,
    "session" TEXT NOT NULL,
    "paper_number" INTEGER NOT NULL,
    "pdf_url" TEXT,
    "total_marks" INTEGER,
    "uploaded_at" TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX "Paper_exam_board_year_session_idx" ON "Paper"("exam_board", "year", "session");

-- Create Question table
CREATE TABLE "Question" (
    "id" TEXT PRIMARY KEY,
    "paper_id" TEXT NOT NULL REFERENCES "Paper"("id") ON DELETE CASCADE,
    "question_number" TEXT NOT NULL,
    "sequence_order" INTEGER NOT NULL,
    "marks" INTEGER
);

CREATE INDEX "Question_paper_id_sequence_order_idx" ON "Question"("paper_id", "sequence_order");

-- Create QuestionContent table
CREATE TABLE "QuestionContent" (
    "id" TEXT PRIMARY KEY,
    "question_id" TEXT NOT NULL REFERENCES "Question"("id") ON DELETE CASCADE,
    "sequence_order" INTEGER NOT NULL,
    "content_type" "ContentType" NOT NULL,
    "text" TEXT,
    "font_size" DOUBLE PRECISION,
    "font_family" TEXT,
    "is_bold" BOOLEAN DEFAULT false,
    "is_italic" BOOLEAN DEFAULT false,
    "x" DOUBLE PRECISION,
    "y" DOUBLE PRECISION,
    "width" DOUBLE PRECISION,
    "height" DOUBLE PRECISION,
    "image_url" TEXT,
    "image_width" INTEGER,
    "image_height" INTEGER,
    "alt_text" TEXT
);

CREATE INDEX "QuestionContent_question_id_sequence_order_idx" ON "QuestionContent"("question_id", "sequence_order");
```

## Step 6: Create Storage Bucket

1. Go to Supabase → Storage
2. Click "New bucket"
3. Name: `question-images`
4. Make it **Public**
5. Click "Create"

## Step 7: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
2. Upload a sample PDF
3. Wait for processing
4. Verify questions are rendered correctly

## 🔄 Automatic Deployments

Every time you push to GitHub, Vercel will automatically:
- Rebuild and redeploy your app
- Generate a preview URL for testing
- Deploy to production if on main branch

## 📊 Vercel Free Tier Limits

- ✅ 100GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Git integration
- ✅ Serverless functions (10s timeout)
- ✅ Edge network (CDN)

**Everything is FREE FOREVER!**

## 🐛 Troubleshooting

### "Failed to upload PDF"

- Check environment variables in Vercel dashboard
- Verify Supabase credentials are correct
- Check function logs in Vercel dashboard

### "Images not loading"

- Verify storage bucket `question-images` is public
- Check CORS settings in Supabase
- Verify `STORAGE_BUCKET` environment variable

### "Database connection error"

- Verify `DATABASE_URL` is correct
- Check Supabase database is not paused
- Ensure tables exist (run Prisma push or SQL)

### Function timeout (10s limit)

This can happen with very large PDFs. Solutions:
1. **Optimize**: Most PDFs parse in 2-5 seconds
2. **Split**: Process one page at a time
3. **Upgrade**: Consider Oracle Cloud VM for unlimited execution time

## 📱 Mobile/Custom Domain

### Add Custom Domain (Free)

1. Go to Vercel project → Settings → Domains
2. Add your domain
3. Update DNS records as instructed
4. Automatic HTTPS certificate

### Progressive Web App (Optional)

Add to `next.config.mjs`:
```javascript
const withPWA = require('next-pwa')({
  dest: 'public'
});

module.exports = withPWA(nextConfig);
```

## 🔐 Security Best Practices

1. **Never commit .env files** (already in .gitignore)
2. **Use environment variables** for all secrets
3. **Rotate Supabase keys** if exposed
4. **Enable rate limiting** in Supabase dashboard
5. **Monitor usage** in Vercel analytics

## ✅ Post-Deployment Checklist

- [ ] Environment variables added to Vercel
- [ ] Database tables created
- [ ] Storage bucket created and public
- [ ] Test upload with sample PDF  
- [ ] Questions render correctly
- [ ] Images load properly
- [ ] Mobile responsive
- [ ] Custom domain configured (optional)

---

**Congratulations!** 🎉 Your PDF parsing system is now live on Vercel with free forever hosting!

Visit https://your-project.vercel.app and start parsing past papers!
