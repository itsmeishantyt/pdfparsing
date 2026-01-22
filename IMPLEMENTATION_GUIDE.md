# Complete Implementation Guide - Start to Finish

This guide will take you from your current state (code on GitHub) to a fully working app deployed on Vercel.

**Time Required:** ~15-20 minutes

---

## Phase 1: Supabase Setup (5 minutes)

### Step 1: Create Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (easiest)

### Step 2: Create a New Project

1. Click "New project"
2. Fill in:
   - **Name:** `economics-parsing` (or anything you like)
   - **Database Password:** Create a strong password (save this!)
   - **Region:** Choose closest to you (e.g., US East, EU West, etc.)
3. Click "Create new project"
4. **Wait 2-3 minutes** for project to initialize

### Step 3: Get Your Credentials

Once your project is ready:

1. Click **Settings** (gear icon in sidebar) → **API**
2. **Copy and save these 3 values:**

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

3. Click **Settings** → **Database**
4. Scroll to "Connection string" → **URI**
5. Copy the connection string and **replace `[YOUR-PASSWORD]` with your actual password**

```
postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Save all 4 values in a notepad - you'll need them soon!**

### Step 4: Create Database Tables

1. Click **SQL Editor** in the left sidebar
2. Click "New query"
3. Copy and paste this entire SQL script:

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

4. Click **RUN** (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

**✅ Database tables created!**

### Step 5: Create Storage Bucket

1. Click **Storage** in the left sidebar
2. Click "Create a new bucket"
3. Fill in:
   - **Name:** `question-images` (must be exactly this)
   - **Public bucket:** ✅ **TURN THIS ON** (important!)
4. Click "Create bucket"

**✅ Storage bucket created!**

---

## Phase 2: Vercel Deployment (5 minutes)

### Step 6: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign up"
3. **Sign up with GitHub** (use same account where you pushed code)

### Step 7: Import Your Project

1. On Vercel dashboard, click "Add New..." → "Project"
2. You'll see your GitHub repos
3. Find **pdfparsing** and click "Import"

### Step 8: Configure Project

Vercel will show project configuration:

1. **Framework Preset:** Should auto-detect "Next.js" ✅
2. **Root Directory:** Leave as `./` ✅
3. **Build Command:** Leave as default ✅
4. **Output Directory:** Leave as default ✅

### Step 9: Add Environment Variables

This is the most important step! Click "Environment Variables" to expand.

Add these **5 variables** (use the values you saved from Supabase):

| Name | Value |
|------|-------|
| `DATABASE_URL` | `postgresql://postgres.xxxxx:[YOUR-PASSWORD]@...` |
| `SUPABASE_URL` | `https://xxxxxxxxxxxxx.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (anon key) |
| `SUPABASE_SERVICE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (service_role key) |
| `STORAGE_BUCKET` | `question-images` |

**How to add each:**
1. Enter **Name** in first box
2. Enter **Value** in second box
3. Click "Add"
4. Repeat for all 5 variables

### Step 10: Deploy!

1. Click **"Deploy"** button at the bottom
2. Vercel will start building...
3. **Wait 2-3 minutes** for deployment to complete
4. You'll see confetti 🎉 when it's done!

**✅ Your app is now live!**

---

## Phase 3: Testing (5 minutes)

### Step 11: Visit Your App

1. Click "Continue to Dashboard"
2. You'll see your deployment with a URL like: `pdfparsing-xxx.vercel.app`
3. Click the **Visit** button or the URL

**You should see the upload page!**

### Step 12: Test PDF Upload

1. **Get a test PDF:**
   - Use any Economics A-level past paper
   - Or use a simple PDF with text and images

2. **Upload the PDF:**
   - Click "Select PDF File"
   - Choose your PDF
   - Fill in metadata:
     - Exam Board: AQA
     - Year: 2023
     - Session: June
     - Paper Number: 1
   - Click "Upload & Parse PDF"

3. **Wait for processing** (5-15 seconds)
   - You'll see "Uploading..."
   - Then automatic redirect

4. **Verify the results:**
   - ✅ Questions are displayed
   - ✅ Question numbers are correct
   - ✅ Images/diagrams are visible
   - ✅ Layout looks good

**If everything works - you're done! 🎉**

---

## Troubleshooting Common Issues

### Issue 1: "Failed to upload PDF"

**Cause:** Environment variables not set correctly

**Fix:**
1. Go to Vercel dashboard
2. Click your project → Settings → Environment Variables
3. Verify all 5 variables are there
4. Check for typos (especially in service_role key)
5. Click "Redeploy" after fixing

### Issue 2: "Database connection error"

**Cause:** DATABASE_URL is wrong

**Fix:**
1. Go back to Supabase → Settings → Database
2. Copy connection string again
3. Make sure you replaced `[YOUR-PASSWORD]` with actual password
4. Update in Vercel environment variables
5. Redeploy

### Issue 3: Images not loading

**Cause:** Storage bucket not public

**Fix:**
1. Go to Supabase → Storage
2. Click on `question-images` bucket
3. Click settings (gear icon)
4. Make sure "Public bucket" is **ON**
5. Try uploading PDF again

### Issue 4: "Question-images bucket not found"

**Cause:** Bucket name mismatch

**Fix:**
1. Check Supabase → Storage
2. Bucket must be named exactly `question-images`
3. If different, either:
   - Rename bucket to `question-images`, OR
   - Update `STORAGE_BUCKET` env var in Vercel
4. Redeploy

### Issue 5: Build fails on Vercel

**Cause:** Missing dependencies or TypeScript errors

**Fix:**
1. Check build logs in Vercel
2. Common fixes:
   - Make sure all files were pushed to GitHub
   - Check that `package.json` is present
   - Redeploy from clean slate

---

## Phase 4: Customization (Optional)

### Add Custom Domain

1. Go to Vercel → Your Project → Settings → Domains
2. Add your domain
3. Update DNS as instructed
4. Wait for SSL certificate (automatic)

### Monitor Usage

**Supabase:**
- Dashboard shows database size
- Storage usage
- API requests

**Vercel:**
- Dashboard shows bandwidth
- Function invocations
- Build minutes

---

## Quick Reference

### Your App URLs

- **Live App:** `https://pdfparsing-xxx.vercel.app`
- **Vercel Dashboard:** `https://vercel.com/dashboard`
- **Supabase Dashboard:** `https://app.supabase.com/project/xxxxx`

### Environment Variables Summary

```env
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=[anon-public-key]
SUPABASE_SERVICE_KEY=[service-role-key]
STORAGE_BUCKET=question-images
```

### Key Files

- `vercel.json` - Vercel configuration
- `api/upload.py` - PDF upload endpoint
- `api/papers.py` - Paper retrieval endpoint
- `prisma/schema.prisma` - Database schema

---

## Next Steps

Now that your app is live:

1. **Test thoroughly** with different PDFs
2. **Share the URL** with others
3. **Monitor usage** in dashboards
4. **Add features** (search, filters, etc.)

### Making Changes

Every time you push to GitHub:
1. Vercel auto-deploys
2. Changes go live in ~2 minutes
3. No manual deployment needed

```bash
# Make changes to code
git add .
git commit -m "Your changes"
git push origin main

# Vercel deploys automatically!
```

---

## Support

If something isn't working:

1. **Check Vercel logs:** Vercel Dashboard → Your Project → Logs
2. **Check Supabase logs:** Supabase Dashboard → Logs
3. **Verify environment variables:** Both platforms
4. **Check this guide:** Re-read relevant section

---

**Congratulations! Your PDF parsing system is now live! 🚀**

Your app: `https://pdfparsing-xxx.vercel.app`

Everything is **FREE FOREVER**:
- ✅ Vercel hosting (100GB bandwidth/month)
- ✅ Supabase database (500MB storage)
- ✅ Supabase storage (1GB files)
- ✅ Automatic HTTPS
- ✅ Global CDN
